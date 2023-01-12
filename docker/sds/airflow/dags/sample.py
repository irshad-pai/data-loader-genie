from airflow.operators.dummy import DummyOperator
from airflow.models.dag import DAG
from datetime import datetime
import json


with DAG(
        dag_id=f"dummy-dag",
        start_date=datetime(2022, 1, 1),
        render_template_as_native_obj=True,
        catchup=False,
        tags=["AUTO-PARSER", "DBT"]
) as dag:

    dummy = DummyOperator(task_id='dummy-task')
    dummy2 = DummyOperator(task_id='dummy-task-2')
    dummy >> dummy2
