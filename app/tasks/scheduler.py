from apscheduler.schedulers.background import BackgroundScheduler

from app.models.comercio.comercio import Comercio
from app.models.processamento.processamento_americanas import ProcessamentoAmericanas
from app.models.processamento.processamento_sem_classificacao import ProcessamentoSemClassificacao
from app.models.processamento.processamento_uvas_mesa import ProcessamentoUvasMesa
from app.models.processamento.processamento_vinifera import ProcessamentoVinifera
from app.models.producao.producao import Producao
from app.services.data_service import run_pipeline

# URLs para os dados
URL_PRODUCAO = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
URL_COMERCIO = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
URL_PROCESSAMENTO_VINIFERA = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
URL_PROCESSAMENTO_AMERICANAS = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"
URL_PROCESSAMENTO_UVAS_MESA = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"
URL_PROCESSAMENTO_SEM_CLASSIFICACAO = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"


# Funções de atualização
def update_producao_data():
    run_pipeline(
        url=URL_PRODUCAO,
        model=Producao,
        id_vars=["id", "control", "produto"],
        id_column="control",
        file_name="producao.csv"
    )


def update_comercio_data():
    run_pipeline(
        url=URL_COMERCIO,
        model=Comercio,
        id_vars=["id", "control", "produto"],
        id_column="control",
        file_name="comercio.csv"
    )


def update_processamento_vinifera():
    run_pipeline(
        url=URL_PROCESSAMENTO_VINIFERA,
        model=ProcessamentoVinifera,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_vinifera.csv"
    )


def update_processamento_americanas():
    run_pipeline(
        url=URL_PROCESSAMENTO_AMERICANAS,
        model=ProcessamentoAmericanas,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_americanas.csv"
    )


def update_processamento_uvas_mesa():
    run_pipeline(
        url=URL_PROCESSAMENTO_UVAS_MESA,
        model=ProcessamentoUvasMesa,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_uvas_mesa.csv"
    )


def update_processamento_sem_classificacao():
    run_pipeline(
        url=URL_PROCESSAMENTO_SEM_CLASSIFICACAO,
        model=ProcessamentoSemClassificacao,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_sem_classificacao.csv"
    )


# Inicia o agendador
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Produção e Comércio
    scheduler.add_job(update_producao_data, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_comercio_data, 'interval', hours=24, max_instances=1)

    # Processamentos
    scheduler.add_job(update_processamento_vinifera, 'interval', hours=23, max_instances=1)
    scheduler.add_job(update_processamento_americanas, 'interval', hours=23, max_instances=1)
    scheduler.add_job(update_processamento_uvas_mesa, 'interval', hours=22, max_instances=1)
    scheduler.add_job(update_processamento_sem_classificacao, 'interval', hours=22, max_instances=1)

    scheduler.start()
    print("Scheduler iniciado. As tarefas serão executadas periodicamente.")
