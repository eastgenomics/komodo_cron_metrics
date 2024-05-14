import argparse
import re


def sanitize_job_name(job_name: str) -> None:
    """
    Make sure the job name doesn't contain forbidden characters
    """
    if not re.match('[a-zA-Z_:][a-zA-Z0-9_:]*', job_name):
        print("The Prometheus job name does not match the required format")
        exit(0)

def get_args():
    """
    Parse the logging path and the job name
    """
    args = argparse.ArgumentParser()
    args.add_argument("log_path", type=str, help="The full path to the \
                      node exporter-monitored logging path")
    args.add_argument("job_name", type=str, help="A string to represent the\
                       job name in Grafana. This must match the requirements\
                       of the Prometheus data model.")
    return args.parse_args()
