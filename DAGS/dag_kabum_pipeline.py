from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

from tasks.scraping import scraping_kabum
from tasks.telegram_notifications import send_telegram
from tasks.util.constants import LOCAL_OUTPUT_PATH, GCS_BUCKET, GCS_OBJECT_PATH, BQ_DEST_TABLE

with DAG(
    'dag_kabum_tv_pipeline',
    default_args={'owner': 'luiz'},
    description='Pipeline modularizada Kabum',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['kabum', 'etl', 'modular']
) as dag:

    scraping_task = PythonOperator(
        task_id='scraping_data',
        python_callable=scraping_kabum
    )

    upload_task = LocalFilesystemToGCSOperator(
        task_id="upload_data",
        src=LOCAL_OUTPUT_PATH,
        dst=GCS_OBJECT_PATH,
        bucket=GCS_BUCKET,
    )

    load_bq_task = GCSToBigQueryOperator(
        task_id="load_bigquery",
        bucket=GCS_BUCKET,
        source_objects=[GCS_OBJECT_PATH],
        destination_project_dataset_table=BQ_DEST_TABLE,
        schema_fields=[
            {"name": "NOME", "type": "STRING", "mode": "NULLABLE"},
            {"name": "PRECO", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "LINK", "type": "STRING", "mode": "NULLABLE"},
            {"name": "IMAGEM", "type": "STRING", "mode": "NULLABLE"},
            {"name": "POLEGADAS", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "MARCA", "type": "STRING", "mode": "NULLABLE"},
            {"name": "PAINEL", "type": "STRING", "mode": "NULLABLE"},
            {"name": "RESOLUCAO", "type": "STRING", "mode": "NULLABLE"},
            {"name": "DATA_EXTRACAO", "type": "STRING", "mode": "NULLABLE"},
        ],
        write_disposition="WRITE_TRUNCATE",
        skip_leading_rows=1,
        source_format="CSV",
    )

    telegram_task = PythonOperator(
        task_id='send_telegram_notification',
        python_callable=send_telegram,
        trigger_rule=TriggerRule.ALL_DONE
    )

    scraping_task >> upload_task >> load_bq_task >> telegram_task
