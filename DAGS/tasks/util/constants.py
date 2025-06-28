from airflow.models import Variable


LOCAL_OUTPUT_PATH = Variable.get("kabum_local_output_path")
GCS_BUCKET = Variable.get("kabum_bucket")
GCS_OBJECT_PATH = Variable.get("kabum_gcs_path")
BQ_DEST_TABLE = Variable.get("kabum_bq_table")
TELEGRAM_TOKEN = Variable.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = Variable.get("TELEGRAM_CHAT_ID")
