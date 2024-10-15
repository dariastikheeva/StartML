from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    "hw_darja-stiheeva-lms4973_9",
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
    def push_xcom(ti):
        ti.xcom_push(
            key="sample_xcom_key",
            value="xcom test"
        )

    task1 = PythonOperator(
        task_id="push_XCom",
        python_callable=push_xcom,
    )

    def pull_xcom(ti):
        res = ti.xcom_pull(
            key="sample_xcom_key",
            task_ids='push_XCom',
        )
        print(res)

    task2 = PythonOperator(
        task_id="pull_XCom",
        python_callable=pull_xcom,
    )
    task1 >> task2
