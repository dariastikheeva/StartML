from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from textwrap import dedent

with DAG(
    'hw_darja-stiheeva-lms4973_1',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
    },
    description='A DAG for homework',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 10, 14),
    catchup=False,
    tags=['hw_1'],
) as dag:
    def print_message(ds, **kwargs):
        print(kwargs)
        print(ds)
        return 'bruh'

    run_this = PythonOperator(
        task_id='print_the_message',
        python_callable=print_message,
    )

    t = BashOperator(
        task_id='print_directory',
        bash_command='pwd ',
        dag=dag,
    )