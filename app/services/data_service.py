import pandas as pd
import os
import requests
from sqlalchemy.orm import Session
from app.database.db import SessionLocal

def download_csv(url, save_dir="tmp", file_name="data.csv"):
    """
    Faz o download do arquivo CSV e salva na pasta especificada.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Arquivo baixado e salvo em: {file_path}")
        return file_path
    else:
        raise Exception(f"Falha ao baixar o arquivo: {response.status_code}")


def process_csv(file_path, id_vars, var_name="ano", value_name="valor"):
    """
    Processa um CSV e converte para formato longo (melt).
    """
    df = pd.read_csv(file_path, delimiter=";")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Converte o DataFrame para formato longo
    long_df = df.melt(
        id_vars=id_vars,
        var_name=var_name,
        value_name=value_name
    )
    long_df[var_name] = long_df[var_name].astype(int)
    long_df[value_name] = pd.to_numeric(long_df[value_name], errors="coerce")
    long_df["control"] = long_df["control"].fillna(long_df["produto"])

    # Remove duplicatas com base no campo de identificação e ano
    long_df = long_df.drop_duplicates(subset=id_vars + [var_name])

    return long_df


def save_data_to_db(data, model, id_column, session: Session):
    """
    Salva os dados processados no banco de dados.
    """
    try:
        new_records = []
        for _, row in data.iterrows():
            # Verifica se o registro já existe
            existing_record = session.query(model).filter_by(
                **{id_column: row[id_column], "ano": row["ano"]}
            ).first()

            if not existing_record:
                new_record = model(
                    **{col: row[col] for col in row.index}
                )
                new_records.append(new_record)

        # Salva novos registros em lote
        if new_records:
            session.bulk_save_objects(new_records)
            session.commit()
            print(f"{len(new_records)} novos registros adicionados!")
        else:
            print("Nenhum novo registro para adicionar.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar os dados: {e}")
    finally:
        session.close()


def run_pipeline(url, model, id_vars, id_column, file_name="data.csv"):
    """
    Pipeline completo para download, processamento e salvamento de dados no banco.
    """
    file_path = ""
    session = SessionLocal()
    try:
        print(f"Iniciando pipeline para {model.__tablename__}...")
        try:
            file_path = download_csv(url, save_dir="tmp", file_name=file_name)
        except Exception as e:
            print(f"Erro ao baixar o arquivo: {e}")
            return
        processed_data = process_csv(file_path, id_vars=id_vars)
        save_data_to_db(processed_data, model=model, session=session)
    except Exception as e:
        print(f"Erro no pipeline: {e}")
    finally:
        session.close()
        print("Pipeline finalizado com sucesso!")
