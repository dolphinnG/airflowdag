import datetime
import pendulum
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunType
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.log.logging_mixin import LoggingMixin

DATA_INTERVAL_START = pendulum.datetime(2021, 9, 13, tz="UTC")
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)

@task.virtualenv(
    task_id='hello_torchx',
    requirements=["torchx"],
    system_site_packages=False,
    execution_timeout=datetime.timedelta(minutes=30),  # Increase timeout as needed
)
def run_torchx(message):
    """This is a function that will run within the DAG execution"""
    from torchx.runner import get_runner
    logger = LoggingMixin().log
    logger.info(f"Running TorchX job with message: {message}")
    with get_runner() as runner:
        # Run the utils.sh component on the local_cwd scheduler.
        app_id = runner.run_component(
            "utils.sh",
            ["echo", message],
            scheduler="local_cwd",
        )

        # Wait for the job to complete
        status = runner.wait(app_id, wait_interval=1)

        # Raise_for_status will raise an exception if the job didn't succeed
        status.raise_for_status()

        # Log the status
        logger.info(f"Job {app_id} completed with status: {status}")

        # Finally we can print all of the log lines from the TorchX job so it
        # will show up in the workflow logs.
        for line in runner.log_lines(app_id, "sh", k=0):
            logger.info(line)

with DAG(
    dag_id='test-torchx3',
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    run_job = run_torchx("Hello, TorchX!")