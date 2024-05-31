import datetime as date
import glob
from pathlib import Path
import os
import re


class Prometheus:
    """
    A class for formatting and writing logs which are readible by Prometheus
    monitoring software. Currently this only logs a 'job completed' message.
    """

    def __init__(
        self,
        out_path: str,
        jobname: str,
    ):
        self.out_path = out_path
        self.jobname = jobname
        self.metrics = []
        self.ppid = os.getppid()
        self.error_filename = f"{self.out_path}/{str(date.datetime.now())}.err"
        self.temp_filename = f"{self.out_path}/{self.jobname}.prom.{self.ppid}"

    def error_if_job_name_invalid(self) -> None:
        """
        Check the job name for forbidden characters.
        Error out with a logged message if not. Make this read-accessible to
        non-cron users.
        """
        regex_pattern = "^[a-zA-Z_:][a-zA-Z0-9_:]*$"
        if not re.match(regex_pattern, self.jobname):
            error = f"The Prometheus job name {self.jobname} does not match "
            + f"the Prometheus data model requirements - it needs to match "
            + f"the regex {regex_pattern}"
            with open(self.error_filename, "a") as new_file:
                new_file.write(error)
            os.chmod(self.error_filename, int("644", base=8))
            exit(0)

    def format_metrics(self) -> None:
        """
        Formats a Prometheus-compatible 'job completed' metric.
        Adds it to a list of ready-to-write metrics.
        """
        timestamp = int(round(date.datetime.now().timestamp()))
        completed_metric = f"{self.jobname}_completed {timestamp}"
        self.metrics.append(completed_metric)

    def emit_temp_metrics(self) -> None:
        """
        Saves the Prometheus metrics to a temporary output prom file.
        """
        # write metric to a temporary path
        with open(self.temp_filename, "a") as new_file:
            for metric in self.metrics:
                new_file.write(metric + "\n")

    def replace_old_metrics(self) -> None:
        """
        Handles the deletion of older metrics ending in *.prom, to prevent
        interference with logging. Renames new metric and sets permissions.
        """
        old_files = glob.glob(f"{self.out_path}/{self.jobname}*.prom")
        if old_files:
            for file in old_files:
                Path(file).unlink()

        new_filename = Path(f"{self.out_path}/{self.jobname}.prom")
        Path(self.temp_filename).rename(new_filename)
        os.chmod(new_filename, int("644", base=8))
