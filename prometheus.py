import datetime as date
import glob
from pathlib import Path
import os


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
        # make sure jobname matches Prom data model (no hyphens)
        self.jobname = jobname
        self.metrics = []
        self.ppid = os.getppid()
        self.temp_filename = f"{self.out_path}/{self.jobname}.prom.{self.ppid}"

    def format_metrics(
            self
    ) -> None:
        """ 
        Formats a Prometheus-compatible 'job completed' metric.
        Adds it to a list of ready-to-write metrics.
        """
        timestamp = int(round(date.datetime.now().timestamp()))
        completed_metric = f"{self.jobname}_completed {timestamp}"
        self.metrics.append(completed_metric)

    def emit_temp_metrics(
            self
    ) -> None:
        """
        Saves the Prometheus metrics to a temporary output prom file.
        """
        # write metric to a temporary path
        with open(self.temp_filename, "a") as new_file:
            for metric in self.metrics:
                new_file.write(metric + "\n")

    def replace_old_metrics(
            self
    ) -> None:
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

