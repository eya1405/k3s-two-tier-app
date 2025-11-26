from flask import Flask, request, render_template_string
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db-service")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "lab5db")
DB_USER = os.getenv("DB_USER", "lab5user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lab5pass")

HTML = """
<!doctype html>
<html>
<head><title>Lab5 Data Form</title></head>
<body>
  <h1>Submit your info</h1>
  <form method="POST" action="/">
    <label>Name:</label><input name="name" required>
    <label>Email:</label><input name="email" type="email" required>
    <button type="submit">Submit</button>
  </form>
  <h2>Stored entries</h2>
  <ul>
    {% for row in rows %}
      <li>{{row[0]}} - {{row[1]}}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS entries (
              name TEXT NOT NULL,
              email TEXT NOT NULL
            );
            """)
            conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO entries (name, email) VALUES (%s, %s)", (name, email))
                conn.commit()
    rows = []
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, email FROM entries ORDER BY name;")
            rows = cur.fetchall()
    return render_template_string(HTML, rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
