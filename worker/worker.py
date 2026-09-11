import os
from consumer import consume

if __name__ == "__main__":
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    print(f"Starting worker, connecting to {host}...")

    consume(host)
