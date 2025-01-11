import shutil

import pandas as pd
import os
import requests
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
import time

from app.utils.file_utils import fix_csv_encoding


def download_csv(url, save_dir="tmp", file_name="data.csv", max_retries=5, retry_interval=2):
    """
    Faz o download do arquivo CSV e salva na pasta especificada, corrigindo encoding.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Arquivo baixado e salvo em: {file_path}")

        retries = 0
        while not os.path.exists(file_path):
            if retries >= max_retries:
                raise Exception("Falha ao garantir que o arquivo foi salvo.")
            retries += 1
            time.sleep(retry_interval)

        # Corrige encoding e caracteres quebrados
        fix_csv_encoding(file_path)

        return file_path
    else:
        raise Exception(f"Falha ao baixar o arquivo: {response.status_code}")


def process_csv(file_path, id_vars, var_name="ano", metric_names=None):
    """
    Processa um CSV de forma genérica, separando múltiplas métricas por ano.

    Args:
        file_path (str): Caminho do arquivo CSV.
        id_vars (list): Colunas que identificam o registro (e.g., 'id', 'pais').
        var_name (str): Nome da coluna representando os anos.
        metric_names (list): Lista de nomes para as métricas detectadas (e.g., ['quantidade_kg', 'valor_usd']).

    Returns:
        pd.DataFrame: DataFrame em formato longo com as métricas separadas.
    """
    if not isinstance(metric_names, list):
        raise ValueError("`metric_names` deve ser uma lista contendo os nomes das métricas.")

    try:
        df = pd.read_csv(file_path, sep=None, engine="python", encoding="latin1")
    except Exception as e:
        raise Exception(f"Erro ao processar o arquivo: {e}")

    # Normaliza nomes das colunas
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df.columns = [col.replace("país", "pais") for col in df.columns]

    # Detecta colunas de quantidade (sem '.1') e de valor (com '.1') apenas se necessário
    quantidade_cols = [col for col in df.columns if col.isdigit() and not col.endswith(".1")]
    valor_cols = [col for col in df.columns if col.endswith(".1")] if len(metric_names) > 1 else []
    print("quantidade_cols:", quantidade_cols)
    print("valor_cols:", valor_cols)

    # Cria DataFrame longo para quantidade
    quantidade_df = df.melt(
        id_vars=id_vars,
        value_vars=quantidade_cols,
        var_name=var_name,
        value_name=metric_names[0]
    )
    quantidade_df[var_name] = quantidade_df[var_name].str.extract(r'(\d+)').astype(int)
    quantidade_df[metric_names[0]] = pd.to_numeric(quantidade_df[metric_names[0]], errors="coerce")

    # Se houver mais de uma métrica, cria DataFrame longo para valores
    if len(metric_names) > 1:
        valor_df = df.melt(
            id_vars=id_vars,
            value_vars=valor_cols,
            var_name=var_name,
            value_name=metric_names[1]
        )
        valor_df[var_name] = valor_df[var_name].str.extract(r'(\d+)').astype(int)
        valor_df[metric_names[1]] = pd.to_numeric(valor_df[metric_names[1]], errors="coerce")

        # Combina quantidade e valor em um único DataFrame
        long_df = pd.merge(quantidade_df, valor_df, on=id_vars + [var_name], how="left")
    else:
        long_df = quantidade_df

    # Remove duplicatas
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
                id=row["id"], ano=row["ano"]
            ).first()

            if existing_record:
                print(f"Registro duplicado encontrado: id={row['id']}, ano={row['ano']}")
            else:
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


def run_pipeline(url, model, id_vars, id_column, file_name="data.csv", metric_names=None):
    """
    Pipeline completo para download, processamento e salvamento de dados no banco.
    """
    save_dir = "tmp"
    session = SessionLocal()
    try:
        print(f"Iniciando pipeline para {model.__tablename__}...")
        file_path = download_csv(url, save_dir=save_dir, file_name=file_name)
        processed_data = process_csv(file_path, id_vars=id_vars, metric_names=metric_names)
        save_data_to_db(processed_data, model=model, id_column=id_column, session=session)
    except Exception as e:
        print(f"Erro no pipeline: {e}")
    finally:
        if os.path.exists(save_dir):
            try:
                # shutil.rmtree(save_dir)
                print(f"Pasta '{save_dir}' removida com sucesso!")
            except Exception as e:
                print(f"Erro ao remover a pasta '{save_dir}': {e}")
        session.close()
        print("Pipeline finalizado com sucesso!")
