import numpy as np
import pandas as pd
import os
import requests
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
import time

from app.utils.file_utils import fix_csv_encoding

def download_csv(url, save_dir="tmp", file_name="data.csv", max_retries=5, retry_interval=2):
    """
    Faz o download de um arquivo CSV, salva em um diretório temporário e corrige problemas de encoding.

    Args:
        url (str): URL de onde o CSV será baixado.
        save_dir (str): Diretório onde o arquivo será salvo (padrão: 'tmp').
        file_name (str): Nome do arquivo salvo (padrão: 'data.csv').
        max_retries (int): Número máximo de tentativas de verificar se o arquivo foi salvo (padrão: 5).
        retry_interval (int): Intervalo (em segundos) entre as tentativas (padrão: 2).

    Returns:
        str: Caminho completo do arquivo salvo.

    Raises:
        Exception: Se o download ou a correção de encoding falharem.
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

        fix_csv_encoding(file_path)

        return file_path
    else:
        raise Exception(f"Falha ao baixar o arquivo: {response.status_code}")


def process_csv(file_path, id_vars, var_name="ano", metric_names=None):
    """
    Processa um arquivo CSV, transformando-o em formato longo e separando métricas, se necessário.

    Args:
        file_path (str): Caminho completo do arquivo CSV.
        id_vars (list): Colunas que identificam os registros (e.g., 'id', 'pais').
        var_name (str): Nome da coluna para os anos (padrão: 'ano').
        metric_names (list): Lista de métricas detectadas no arquivo.

    Returns:
        pd.DataFrame: DataFrame processado em formato longo.

    Raises:
        ValueError: Se `metric_names` não for uma lista.
        Exception: Se houver erro ao processar o arquivo.
    """
    if not isinstance(metric_names, list):
        raise ValueError("`metric_names` deve ser uma lista contendo os nomes das métricas.")

    try:
        df = pd.read_csv(file_path, sep=None, engine="python", encoding="latin1")
    except Exception as e:
        raise Exception(f"Erro ao processar o arquivo: {e}")

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df.columns = [col.replace("país", "pais") for col in df.columns]

    quantidade_cols = [col for col in df.columns if col.isdigit() and not col.endswith(".1")]
    valor_cols = [col for col in df.columns if col.endswith(".1")] if len(metric_names) > 1 else []

    quantidade_df = df.melt(
        id_vars=id_vars,
        value_vars=quantidade_cols,
        var_name=var_name,
        value_name=metric_names[0]
    )

    quantidade_df[var_name] = quantidade_df[var_name].str.extract(r'(\d+)').astype(int)
    quantidade_df[metric_names[0]] = pd.to_numeric(quantidade_df[metric_names[0]], errors="coerce")

    if len(metric_names) > 1:
        valor_df = df.melt(
            id_vars=id_vars,
            value_vars=valor_cols,
            var_name=var_name,
            value_name=metric_names[1]
        )
        valor_df[var_name] = valor_df[var_name].str.extract(r'(\d+)').astype(int)
        valor_df[metric_names[1]] = pd.to_numeric(valor_df[metric_names[1]], errors="coerce")

        long_df = pd.merge(quantidade_df, valor_df, on=id_vars + [var_name], how="left")
    else:
        long_df = quantidade_df

    long_df = long_df.drop_duplicates(subset=id_vars + [var_name])

    return long_df


def save_data_to_db(data, model, id_column, session: Session):
    """
    Salva os dados processados no banco de dados, evitando duplicatas.

    Args:
        data (pd.DataFrame): Dados processados a serem salvos.
        model (SQLAlchemy Model): Modelo da tabela no banco de dados.
        id_column (str): Nome da coluna identificadora no modelo.
        session (Session): Sessão ativa do banco de dados.

    Raises:
        Exception: Se houver erro ao salvar os dados.
    """
    try:
        data = data.replace({np.nan: None})

        new_records = []
        for _, row in data.iterrows():
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
    Executa o pipeline completo para download, processamento e armazenamento no banco de dados.

    Args:
        url (str): URL do arquivo CSV.
        model (SQLAlchemy Model): Modelo da tabela no banco de dados.
        id_vars (list): Colunas identificadoras no DataFrame.
        id_column (str): Coluna identificadora no banco de dados.
        file_name (str): Nome do arquivo salvo localmente (padrão: 'data.csv').
        metric_names (list): Lista de métricas detectadas no arquivo.

    Raises:
        Exception: Se houver erro em qualquer etapa do pipeline.
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
        session.close()
        print("Pipeline finalizado com sucesso!")
