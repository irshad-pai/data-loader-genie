from airflow.models.dag import DAG
import json
from datetime import datetime
import os
from airflow.operators.bash import BashOperator
from jinja2 import Template
import pendulum

class AirflowConstants:
    SDM_DBT_PROJECT_DIRECTORY_ENV_VAR="SDS_SDM_DBT_PROJECT_DIRECTORY"
    SDS_WAREHOUSE_PATH_ENV_VAR="SDS_WAREHOUSE_PATH"
    ARTIFACTORY_ENV_VAR="SDS_ARTIFACTORY_PATH"


def render_variable(variable, task_instance):
    """Renders Jinja templating over the 'variable' parameter passed to the function by applying templates
    available in airflow and the user defined macros defined in a DAG

    Args:
        variable (string): Jinja format templated string
        task_instance (TaskInstance): Task instance object for a given task

    Returns:
        [string]: Returns templated object as a string
    """
    jn = Template(variable)
    macros = task_instance.get_template_context()['dag'].user_defined_macros
    return jn.render(**task_instance.get_template_context(), **macros)

with DAG(
        dag_id=f"$source-autoparser-dag",
        start_date=datetime(2022, 1, 1),
        schedule_interval= $cron,
        render_template_as_native_obj=True,
        catchup=False,
        user_defined_macros={
            "json": json,
            "pendulum": pendulum,
            "os": os,
            "render_variable": render_variable()
        },
        tags=["AUTO-PARSER", "DBT"]
) as dag:
    srdm_task = BashOperator(task_id=f"$source-srdm-population",
                             bash_command=f"spark-submit --class $className "
                                          f"--conf --master local --driver-memory 2g --driver-cores 1 --executor-cores 1 --jars {{{{os.getenv('{AirflowConstants.ARTIFACTORY_ENV_VAR}','/opt/airflow/dbt')}}}}"
                                          f"--spark-service spark --config-path  --modified-after {{{{data_interval_start.to_iso8601_string().split('.')[0]}}}} --modified-before {{{{data_interval_start.to_iso8601_string().split('.')[0]}}}}")

    bash_command_run = (
        f"cd \"{{{{os.getenv('{AirflowConstants.SDM_DBT_PROJECT_DIRECTORY_ENV_VAR}','/opt/airflow/dbt')}}}}\""
        f"&& dbt run --models $sdmName"
        f" --vars '{{"
        f"\"schema_location\":\"{{{{os.getenv('{AirflowConstants.SDS_WAREHOUSE_PATH_ENV_VAR}','s3a://')}}}}\" }}' "
        f"\"schema_name\":\"sdm\""
    )

    sdm_task = BashOperator(task_id=f"$source-sdm-population",
                            bash_command=bash_command_run)

    srdm_task >> sdm_task