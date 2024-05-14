from bin.prometheus import Prometheus
from bin.args import get_args


def main():
    args = get_args()
    prom = Prometheus("/prom_metrics", args.job_name)
    prom.format_metrics()
    prom.emit_temp_metrics()
    prom.replace_old_metrics()


if __name__ == "__main__":
    main()
