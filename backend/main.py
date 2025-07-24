from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS  # CORS 허용을 위한 설정
import time

app = Flask(__name__)
CORS(app)  # 프론트에서 API 호출 가능하게 CORS 허용

# DB 연결 재시도 함수
def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="counterdb",
                user="myuser",
                password="mypass",
                host="db",
                port=5432
            )
            print("✅ DB 연결 성공!")
            return conn
        except OperationalError as e:
            print("❌ DB 연결 실패:", e)
            print("3초 후 다시 시도합니다...")
            time.sleep(3)

# PostgreSQL 연결 설정
conn = connect_to_db()
cur = conn.cursor()

# 테이블이 없다면 생성
cur.execute("""
    CREATE TABLE IF NOT EXISTS counters (
        id SERIAL PRIMARY KEY,
        name TEXT,
        count INT
    );
""")
conn.commit()

# ✅ 버튼 클릭 시 호출되는 POST API → 카운트 증가
@app.route("/count/<name>", methods=["POST"])
def increment(name):
    # 해당 이름의 카운트를 조회
    cur.execute("SELECT count FROM counters WHERE name=%s;", (name,))
    result = cur.fetchone()

    if result:
        new_count = result[0] + 1
        cur.execute("UPDATE counters SET count=%s WHERE name=%s;", (new_count, name))
    else:
        new_count = 1
        cur.execute("INSERT INTO counters (name, count) VALUES (%s, %s);", (name, new_count))

    conn.commit()
    return jsonify({"name": name, "count": new_count})

# ✅ 카운트 조회용 GET API
@app.route("/count/<name>", methods=["GET"])
def get_count(name):
    cur.execute("SELECT count FROM counters WHERE name=%s;", (name,))
    result = cur.fetchone()
    return jsonify({"name": name, "count": result[0] if result else 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 외부에서 접근 가능하게 설정
