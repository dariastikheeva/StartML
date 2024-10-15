from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from textwrap import dedent

with DAG(
    "hw_darja-stiheeva-lms4973_5",
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
    },
    description="A DAG for homework",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 10, 14),
    catchup=False,
) as dag:
    templated_command = dedent(
        '''
        {% for i in range(5) %}
            echo '{{ ts }}'
            echo '{{ run_id }}'
        {% endfor %}
        '''
    )
