import argparse


def get_args():
    """
    Parse the logging path and the job name
    """
    args = argparse.ArgumentParser()
    args.add_argument(
        "job_name",
        type=str,
        help="A string to represent the job name in Grafana. This must"
        " match the requirements of the Prometheus data model.",
    )
    return args.parse_args()
