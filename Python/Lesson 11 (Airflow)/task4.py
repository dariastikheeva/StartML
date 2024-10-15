from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from textwrap import dedent

with DAG(
    "hw_darja-stiheeva-lms4973_3",
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
        t1 = BashOperator(
            task_id=f'dag_bash_{i}',
            bash_command=f'echo {i}',
        )

    def print_task_num(task_number):
        print(f'task number is: {task_number}')

    for i in range(20):
        t2 = PythonOperator(
            task_id=f'dag_python_{10 + i}',
            python_callable=print_task_num,
            op_kwargs={'task_number': 10 + i}
        )
    t1.doc_md = dedent(
        '''
        # Bash Operator documentation

        Create **10 tasks** using `bash_command=f'echo {i}` where *i* is a task id

        '''
    )

    t2.doc_md = dedent(
        '''
        # Python Operator documentation

        Create **20 tasks** using `task_id=f'dag_python_{10 + i}` and *print_task_num* function

        '''
    )
    
