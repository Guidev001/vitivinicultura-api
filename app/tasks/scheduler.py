from apscheduler.schedulers.background import BackgroundScheduler

from app.services.producao_service import process_producao_csv, save_producao_to_db, download_csv

URL = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"  # URL do arquivo

def update_producao_data():
    """
    Pipeline completo: baixa o CSV, processa e salva no banco de dados.
    """
    print("Iniciando atualização dos dados de Produção...")
    try:
        file_path = download_csv(URL, save_dir="tmp", file_name="producao.csv")
        producao_data = process_producao_csv(file_path)
        save_producao_to_db(producao_data)
        print("Atualização concluída com sucesso!")
    except Exception as e:
        print(f"Erro no pipeline: {e}")

def start_scheduler():
    """
    Inicia o agendador de tarefas em background.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_producao_data, 'interval', minutes=10)
    scheduler.start()
    print("Scheduler iniciado. A tarefa será executada a cada 1 minuto.")
