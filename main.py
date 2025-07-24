import os
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Definição dos Jobs ---

def job_cada_10_segundos():
    """
    Job 1: Uma tarefa que executa frequentemente.
    """
    print(f"[JOB 1 - 10s] Executando... Hora: {datetime.now().strftime('%H:%M:%S')}")

def job_do_meio_dia():
    """
    Job 2: Uma tarefa que executa uma vez por dia.
    """
    print(f"☀️ [JOB 2 - Meio-Dia] Hora do almoço! Executado às: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """
    Função principal que configura e inicia o agendador com múltiplos jobs.
    """
    # 1. Carrega as configurações de agendamento do .env
    cron_10_segundos = os.getenv('CRON_JOB_1_CADA_10_SEGUNDOS')
    cron_meio_dia = os.getenv('CRON_JOB_2_MEIO_DIA')

    # Validação para garantir que as variáveis foram carregadas
    if not all([cron_10_segundos, cron_meio_dia]):
        print("Erro: Verifique se as variáveis de ambiente CRON_JOB_1 e CRON_JOB_2 estão definidas no arquivo .env.")
        return

    # 2. Inicializa um único agendador
    # A hora atual é 18:47 em Manaus (GMT-4).
    scheduler = BlockingScheduler(timezone='America/Manaus')
    print("Agendador iniciado com 2 jobs. Pressione Ctrl+C para sair.")

    try:
        # 3. Adiciona o primeiro job (a cada 10 segundos)
        scheduler.add_job(
            job_cada_10_segundos,
            CronTrigger.from_crontab(cron_10_segundos, timezone='America/Manaus')
        )
        print(f"-> Job 1 agendado com a regra: '{cron_10_segundos}'")

        # 4. Adiciona o segundo job (ao meio-dia)
        scheduler.add_job(
            job_do_meio_dia,
            CronTrigger.from_crontab(cron_meio_dia, timezone='America/Manaus')
        )
        print(f"-> Job 2 agendado com a regra: '{cron_meio_dia}'")

        # 5. Inicia o agendador
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        print("\nAgendador parado.")
        scheduler.shutdown()

if __name__ == '__main__':
    main()