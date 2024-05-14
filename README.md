# komodo_cron_metrics

## Purpose
A Python script which writes a timestamped Prometheus 'job completed' metric when a komodo-monitored cron job completes successfully. Because Prometheus can only handle one copy of a metric for the same job,
the script makes a temporary file, deletes the old metric file, and renames the new file
accordingly.

It is intended to be used in crontab commands, as a 'second call' in the event of a successful cron job. In the example below, if the 'my_app' Docker runs and closes successfully (exit code 0), then the komodo_cron_metrics script will run. If 'my_app' fails to run correctly (exit code other than 0) or doesn't run, then komodo_cron_metrics won't run:
```
0 0 * * 1 docker run --rm my_app && docker run --rm komodo_run_metrics
```
Prometheus can be configured to issue alerts if the targeted cron job doesn't run in the expected timeframe. In that case, if 'my_app' runs weekly, and Prometheus detects that the last metric for 'my_app' is over 7.5 days ago, Prometheus will send a Slack alert.


## Input
The script takes two arguments:
- The path to the output directory for Prometheus metrics. You'll need to ensure this directory is monitored by Node Exporter in order for Prometheus to collect the metrics.
- The job name, which will be prepended to the '_completed' metric. Please heed the Prometheus metric naming documentation: https://prometheus.io/docs/practices/naming/ Metrics must match the regex '[a-zA-Z_:][a-zA-Z0-9_:]*'.

The most basic possible example call is as follows:
```
python /path/to/komodo_cron_metrics/main.py /monitored/output/path my_app_name
```

## Output
The above code will write out a file named 'my_app_name.prom' to '/monitored/output/path'.
The file will contain the metric with '_completed' appended to it, followed by a space, and then the epoch time at which the script was called.
For example:
```
my_app_name_completed 1715694964
```
