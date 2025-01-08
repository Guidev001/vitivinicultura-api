from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_service import run_pipeline
from app.models.producao import Producao
from app.models.comercio import Comercio

URL_PRODUCAO = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
URL_COMERCIO = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"

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

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_producao_data, 'interval', minutes=3)
    scheduler.add_job(update_comercio_data, 'interval', minutes=3)
    scheduler.start()
    print("Scheduler iniciado. As tarefas serão executadas periodicamente.")
