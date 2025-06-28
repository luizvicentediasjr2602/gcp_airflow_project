import requests
from airflow.models import Variable
from airflow.utils.dates import timezone

def send_telegram(**context):
    token = Variable.get("TELEGRAM_TOKEN")
    chat_id = Variable.get("TELEGRAM_CHAT_ID")

   
    dag_id = context['dag'].dag_id
    exec_date = context['execution_date'].strftime('%Y-%m-%d %H:%M:%S')
    status = 'SUCESSO'

   
    qtd_produtos = context['ti'].xcom_pull(task_ids='scraping_data', key='qtd_produtos') or 'N/A'

    message = (
        f"*Relatório de Execução - Kabum ETL*\n\n"
        f"*DAG:* `{dag_id}`\n"
        f"*Status:* {status}\n"
        f"*Execução:* `{exec_date}`\n"
        f"*Produtos extraídos:* `{qtd_produtos}`\n"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        raise Exception(f"Erro ao enviar mensagem no Telegram: {resp.text}")
