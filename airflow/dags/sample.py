from airflow import DAG
from airflow.operators import PythonOperator

from datetime import datetime


def sample_function():
    pass


default_args = {
    'owner': 'Naren',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email': [''],  # email here
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 0,
}

with DAG(
    'DAGName',
    default_args=default_args,
    schedule_interval='*/5 9-17 * * *',  # cron schedule
    catchup=False,
) as dag:
    price_listener = PythonOperator(
        task_id='listener',
        python_callable=sample_function,
    )
