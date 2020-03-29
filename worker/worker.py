import json
import os
import redis
from time import sleep
from random import randint

if __name__ == "__main__":
    redis_host = os.getenv("REDIS_HOST", "queue")
    r = redis.Redis(host=redis_host, port=6379, db=0)
    print("Aguardando...")
    while True:
        message = json.loads(r.blpop("sender")[1])
        # Mail send simulate
        print(f"Sending message {message['assunto']}")
        sleep(randint(15, 45))
        print(f"Sended message {message['assunto']}")
