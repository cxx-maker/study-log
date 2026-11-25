import pymysql
from pathlib import Path


def load_env(path):
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


BASE_DIR = Path(__file__).resolve().parent.parent
ENV = load_env(BASE_DIR / ".env")

CONFIG = {
    "host": ENV["DB_HOST"],
    "port": int(ENV["DB_PORT"]),
    "user": ENV["DB_USER"],
    "password": ENV["DB_PASSWORD"],
    "database": ENV["DB_NAME"],
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_conn():
    return pymysql.connect(**CONFIG)


def query(sql):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()
def execute(sql):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        return True
    finally:
        conn.close()


if __name__ == "__main__":
   print(execute("DELETE FROM orders WHERE amount = 10.00"))
   print(query("SELECT COUNT(*) AS c FROM orders"))
