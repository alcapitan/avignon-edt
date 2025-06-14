import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg
from flask import Flask, request, jsonify

# Chargement du .env
load_dotenv()

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )


app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint introuvable."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erreur interne du serveur."}), 500

@app.route('/api/list/<item>', methods=['GET'])
def get_list(item):
    # Mappage entre les éléments d'URL et les colonnes SQL
    valid_items = {
        "ue": "ue_name",
        "group": "UNNEST(class_group)",
        "teacher": "UNNEST(teacher)",
        "classroom": "classroom_id"
    }

    if item not in valid_items:
        return jsonify({"error": "Item invalide. Utilisez 'ue', 'group', 'classroom' ou 'teacher'."}), 400

    column_expr = valid_items[item]

    query = f"""
    SELECT DISTINCT {column_expr} AS value
    FROM classroom_events
    WHERE {column_expr} IS NOT NULL
    ORDER BY value;
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                results = [row[0] for row in rows if row[0] is not None]
        return jsonify(results)
    except psycopg.Error as e:
        return jsonify({"error": f"Erreur serveur lors de la récupération des {item}s : {e}"}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    classroom = request.args.get('classroom')
    ue = request.args.get('ue')
    group = request.args.get('group')
    teacher = request.args.get('teacher')
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
        filters.append("%s::text = ANY(class_group)")
        params.append(group)
    
    if teacher:
        filters.append("%s::text = ANY(teacher)")
        params.append(teacher)

    if date:
        try:
            date_obj = datetime.fromisoformat(date).date()
            filters.append("date_start::date <= %s AND %s <= date_end::date")
            params.extend([date_obj, date_obj])

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
    try:
        with get_db_connection() as conn:
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                # results = [dict(zip(columns, row)) for row in rows]
                results = []
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    # Normaliser les dates si elles existent
                    if 'date_start' in row_dict and isinstance(row_dict['date_start'], (datetime,)):
                        row_dict['date_start'] = row_dict['date_start'].isoformat()
                    if 'date_end' in row_dict and isinstance(row_dict['date_end'], (datetime,)):
                        row_dict['date_end'] = row_dict['date_end'].isoformat()
                    results.append(row_dict)
        return jsonify(results)
    except psycopg.Error as e:
        return jsonify({"error": f"Erreur serveur lors de la récupération des événements : {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
