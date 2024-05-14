# komodo_cron_metrics

## Purpose
A Python script which writes a timestamped Prometheus 'job completed' metric when a komodo-monitored cron job completes successfully. Because Prometheus can only handle one copy of a metric for the same job,
the script makes a temporary file, deletes the old metric file, and renames the new file
accordingly.

It is intended to be used in crontab commands, as a second call in the event of a successful cron job (e.g. after &&).Prometheus can be configured to issue alerts if the targeted cron job doesn't run in the expected timeframe. In that case, if 'my_app' runs weekly, and Prometheus detects that the last metric for 'my_app' is over 7.5 days ago, Prometheus will send a Slack alert.


## Set-up
The script is designed to be built into a Docker container. If not experienced, follow this 'build the app's image' guide from step 3: https://docs.docker.com/get-started/02_our_app/#build-the-apps-image


## Input
The script takes one argument:
- job_name: this will be prepended to the '_completed' metric. Please note that the Prometheus metric naming documentation must be followed: https://prometheus.io/docs/practices/naming/ Metrics must match the regex '[a-zA-Z_:][a-zA-Z0-9_:]*'.

When you run the script as a containerised application, you must also provide:
- ```-v```: to mount the container's output path, ```/prom_metrics```, to the path which is monitored by Node Exporter.


## Example
A basic example call is as follows:
```
docker run --rm -v /path/to/my/prom_logs:/prom_metrics komodo_cron_metrics my_app_name
```
Or, when set up to log completion of the weekly-running 'my_app_name' in a crontab:
```
0 8 * * 1 docker run --rm my_app_name:1.0.5 && docker run --rm -v /path/to/my/prom_logs:/prom_metrics komodo_cron_metrics my_app_name
```


## Output
The above code will write out a file named 'my_app_name.prom' to '/path/to/my/prom_logs'.
The file will contain the metric with '_completed' appended to it, followed by a space, and then the epoch time at which the script was called.
For example:
```
my_app_name_completed 1715694964
```
