import psycopg2
import redis
import json
import os
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route("/", method="POST", callback=self.send)
        host_redis = self.get_host_redis()
        self.file = redis.StrictRedis(host=host_redis, port=6379, db=0)
        self.conn = psycopg2.connect(self.get_dsn())

    def get_dsn(self):
        db_host = os.getenv("DB_HOST", "db")
        db_user = os.getenv("DB_USER", "postgres")
        db_name = os.getenv("DB_NAME", "email_sender")
        return f"dbname={db_name} user={db_user} host={db_host}"

    def get_host_redis(self):
        return os.getenv("HOST_REDIS", "queue")

    def register_message(self, subject, message):
        SQL = "INSERT INTO emails (assunto, menssagem) VALUES (%s, %s)"
        cur = self.conn.cursor()
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {"assunto": subject, "menssagem": message}
        self.file.rpush("sender", json.dumps(msg))
        print("Registred message!")

    def send(self):
        subject = request.forms.get("subject")
        message = request.forms.get("message")

        self.register_message(subject, message)

        return "Menssagem enfileirada! Assunto: {}, menssagem: {}".format(
            subject, message
        )


if __name__ == "__main__":
    sender = Sender()
    sender.run(host="0.0.0.0", port=8080, debug=True)
