from apscheduler.schedulers.background import BackgroundScheduler

from app.models.comercio.comercio import Comercio
from app.models.exportacao.exportacao_espumantes import ExportacaoEspumantes
from app.models.exportacao.exportacao_frescas import ExportacaoFrescas
from app.models.exportacao.exportacao_suco import ExportacaoSuco
from app.models.exportacao.exportacao_vinhos import ExportacaoVinhos
from app.models.importacao.importacao_espumantes import ImportacaoEspumantes
from app.models.importacao.importacao_frescas import ImportacaoFrescas
from app.models.importacao.importacao_passas import ImportacaoPassas
from app.models.importacao.importacao_suco import ImportacaoSuco
from app.models.importacao.importacao_vinhos import ImportacaoVinhos
from app.models.processamento.processamento_americanas import ProcessamentoAmericanas
from app.models.processamento.processamento_sem_classificacao import ProcessamentoSemClassificacao
from app.models.processamento.processamento_uvas_mesa import ProcessamentoUvasMesa
from app.models.processamento.processamento_vinifera import ProcessamentoVinifera
from app.models.producao.producao import Producao
from app.services.data_service import run_pipeline

URL_PRODUCAO = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
URL_COMERCIO = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"

URL_PROCESSAMENTO_VINIFERA = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
URL_PROCESSAMENTO_AMERICANAS = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"
URL_PROCESSAMENTO_UVAS_MESA = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"
URL_PROCESSAMENTO_SEM_CLASSIFICACAO = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"

URL_IMPORTACAO_VINHOS = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
URL_IMPORTACAO_SUCO = "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv"
URL_IMPORTACAO_FRESCAS = "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv"
URL_IMPORTACAO_ESPUMANTES = "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv"
URL_IMPORTACAO_PASSAS = "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv"

URL_EXPORTACAO_VINHOS = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
URL_EXPORTACAO_SUCO = "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"
URL_EXPORTACAO_ESPUMANTES = "http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv"
URL_EXPORTACAO_PASSAS = "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv"

# Funções de atualização
def update_producao_data():
    run_pipeline(
        url=URL_PRODUCAO,
        model=Producao,
        id_vars=["id", "control", "produto"],
        id_column="control",
        file_name="producao.csv",
        metric_names=["litros"]
    )


def update_comercio_data():
    run_pipeline(
        url=URL_COMERCIO,
        model=Comercio,
        id_vars=["id", "control", "produto"],
        id_column="control",
        file_name="comercio.csv",
        metric_names=["litros"]
    )


def update_processamento_vinifera():
    run_pipeline(
        url=URL_PROCESSAMENTO_VINIFERA,
        model=ProcessamentoVinifera,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_vinifera.csv",
        metric_names=["kg"]
    )


def update_processamento_americanas():
    run_pipeline(
        url=URL_PROCESSAMENTO_AMERICANAS,
        model=ProcessamentoAmericanas,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_americanas.csv",
        metric_names=["kg"]
    )


def update_processamento_uvas_mesa():
    run_pipeline(
        url=URL_PROCESSAMENTO_UVAS_MESA,
        model=ProcessamentoUvasMesa,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_uvas_mesa.csv",
        metric_names=["kg"]
    )


def update_processamento_sem_classificacao():
    run_pipeline(
        url=URL_PROCESSAMENTO_SEM_CLASSIFICACAO,
        model=ProcessamentoSemClassificacao,
        id_vars=["id", "control", "cultivar"],
        id_column="control",
        file_name="processamento_sem_classificacao.csv",
        metric_names=["kg"]
    )

def update_imp_frescas():
    run_pipeline(
        url=URL_IMPORTACAO_FRESCAS,
        model=ImportacaoFrescas,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="imp_frescas.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_imp_vinhos():
    run_pipeline(
        url=URL_IMPORTACAO_VINHOS,
        model=ImportacaoVinhos,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="imp_vinhos.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_imp_suco():
    run_pipeline(
        url=URL_IMPORTACAO_SUCO,
        model=ImportacaoSuco,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="imp_suco.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_imp_espumantes():
    run_pipeline(
        url=URL_IMPORTACAO_ESPUMANTES,
        model=ImportacaoEspumantes,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="imp_espumantes.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_imp_passas():
    run_pipeline(
        url=URL_IMPORTACAO_PASSAS,
        model=ImportacaoPassas,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="imp_passas.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_exp_vinhos():
    run_pipeline(
        url=URL_EXPORTACAO_VINHOS,
        model=ExportacaoVinhos,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="exp_vinhos.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_exp_suco():
    run_pipeline(
        url=URL_EXPORTACAO_SUCO,
        model=ExportacaoSuco,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="exp_suco.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_exp_espumantes():
    run_pipeline(
        url=URL_EXPORTACAO_ESPUMANTES,
        model=ExportacaoEspumantes,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="exp_espumantes.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )

def update_exp_frescas():
    run_pipeline(
        url=URL_EXPORTACAO_PASSAS,
        model=ExportacaoFrescas,
        id_vars=["id", "pais"],
        id_column="pais",
        file_name="exp_passas.csv",
        metric_names=["quantidade_kg", "valor_usd"]
    )




def start_scheduler():
    scheduler = BackgroundScheduler()

    # Produção e Comércio
    scheduler.add_job(update_producao_data, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_comercio_data, 'interval', hours=24, max_instances=1)

    # Processamentos
    scheduler.add_job(update_processamento_vinifera, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_processamento_americanas, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_processamento_uvas_mesa, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_processamento_sem_classificacao, 'interval', hours=24, max_instances=1)

    # Importações
    scheduler.add_job(update_imp_frescas, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_imp_vinhos, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_imp_suco, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_imp_espumantes, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_imp_passas, 'interval', hours=24, max_instances=1)

    # Exportações
    scheduler.add_job(update_exp_vinhos, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_exp_suco, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_exp_espumantes, 'interval', hours=24, max_instances=1)
    scheduler.add_job(update_exp_frescas, 'interval', hours=24, max_instances=1)

    scheduler.start()
    print("Scheduler iniciado. As tarefas serão executadas periodicamente.")
