import logging

from prometheus_client import start_http_server

from executor.config import METRICS_PORT
from executor.worker import run_forever


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    start_http_server(METRICS_PORT)
    run_forever()


if __name__ == "__main__":
    main()
