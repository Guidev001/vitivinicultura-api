import pandas as pd
import os
import requests

from app.models.producao import Producao
from app.database.db import SessionLocal

def download_csv(url, save_dir="tmp", file_name="producao.csv"):
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

def process_producao_csv(file_path):
    """
    Processa o CSV de Produção e converte para formato longo (melt).
    """
    df = pd.read_csv(file_path, delimiter=";")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Converte o DataFrame para formato longo
    long_df = df.melt(
        id_vars=["id", "control", "produto"],
        var_name="ano",
        value_name="valor"
    )
    long_df["ano"] = long_df["ano"].astype(int)
    long_df["valor"] = pd.to_numeric(long_df["valor"], errors="coerce")

    # Remove duplicatas com base no campo 'id' e 'ano'
    long_df = long_df.drop_duplicates(subset=["id", "ano"])

    return long_df


def save_producao_to_db(data):
    """
    Salva os dados processados no banco de dados.
    """
    session = SessionLocal()
    try:
        for _, row in data.iterrows():
            existing_record = session.query(Producao).filter_by(
                vinho_id=row["id"],
                ano=row["ano"]
            ).first()

            if not existing_record:
                new_record = Producao(
                    vinho_id=row["id"],
                    control=row["control"],
                    produto=row["produto"],
                    ano=row["ano"],
                    valor=row["valor"]
                )
                print(f"Novo registro adicionado: vinho_id={new_record.vinho_id}, ano={new_record.ano}")
                session.add(new_record)

        session.commit()
        print("Dados atualizados no banco de dados!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar os dados: {e}")
    finally:
        session.close()

