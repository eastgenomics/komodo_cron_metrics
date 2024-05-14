from prometheus import Prometheus
from args import parse_args

def main():
    args = parse_args()
    prom = Prometheus(args.log_path, args.job_name)
    prom.format_metrics
    prom.emit_temp_metrics
    prom.replace_old_metrics


if __name__ == "__main__":
    main()
