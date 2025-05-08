import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg
from flask import Flask, request, jsonify

# Chargement du .env
load_dotenv()

# Connexion Postgres
conn = psycopg.connect(
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT"),
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD")
)

app = Flask(__name__)

@app.route('/api/events', methods=['GET'])
def get_events():
    classroom = request.args.get('classroom')
    ue = request.args.get('ue')
    group = request.args.get('group')
    date = request.args.get('date')

    filters = []
    params = []

    if classroom:
        filters.append("classroom_id = %s")
        params.append(classroom)

    if ue:
        filters.append("ue_name = %s")
        params.append(ue)

    if group:
        filters.append("class_group = %s")
        params.append(group)

    if date:
        try:
            date_obj = datetime.fromisoformat(date).date()
            filters.append("%s BETWEEN date_start::date AND date_end::date")
            params.append(date_obj)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    query = f"""
    SELECT event_id, classroom_id, ue_name, teacher, class_group, 
           date_start, date_end, type
    FROM classroom_events
    {where_clause}
    ORDER BY date_start ASC;
    """

    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in rows]

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
