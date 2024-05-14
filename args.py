import argparse


def sanitize_job_name():
    """
    Make sure the job name doesn't contain forbidden characters
    """

def parse_args():
    """
    Parse the logging path and the job name
    """
    args = argparse.ArgumentParser()
    args.add_argument("log_path", type=str, help="The full path to the \
                      node exporter-monitored logging path")
    args.add_argument("job_name", type=str, help="A string to represent the\
                       job name. Note this will be displayed in Grafana, \
                      so please make it obvious which app is being run")
    return args.parse_args()
