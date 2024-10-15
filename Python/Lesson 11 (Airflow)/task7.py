from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    "hw_darja-stiheeva-lms4973_7",
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
    for i in range(10):
        t = BashOperator(
            task_id=f'dag_bash_{i}',
            bash_command=f'echo {i}',
        )

    def print_task_num(ts, run_id, **kwargs):
        print(ts)
        print(run_id)

    for i in range(20):
        t = PythonOperator(
            task_id=f'dag_python_{i}',
            python_callable=print_task_num,
            op_kwargs={'task_number': i}
        )
