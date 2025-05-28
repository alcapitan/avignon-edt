#! /usr/bin/env python3

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import requests
import psycopg
from icalendar import Calendar

load_dotenv()  # charge les variables du fichier .env

def parse_event(vevent, classroom_id):
    uid = str(vevent.get('UID'))
    description = str(vevent.get('DESCRIPTION', ''))
    dtstart = vevent.decoded('DTSTART')
    dtend = vevent.decoded('DTEND')
    last_modified = vevent.get('LAST-MODIFIED')
    date_update = last_modified.dt if last_modified else datetime.now(timezone.utc)

    # Parsing DESCRIPTION
    desc_lines = description.splitlines()
    ue_name = ''
    teacher_list = []
    class_group_list = []
    event_type = ''

    for line in desc_lines:
        if line.startswith('Matière'):
            ue_name = line.split(':', 1)[1].strip()
        elif line.startswith('Enseignant'):
            teacher_string = line.split(':', 1)[1].strip()
            teacher_list = [teacher.strip() for teacher in teacher_string.split(',')]
        elif line.startswith('TD') or line.startswith('Promotion'):
            class_group_string = line.split(':', 1)[1].strip()
            class_group_list = [group.strip() for group in class_group_string.split(',')]
        elif line.startswith('Type'):
            event_type = line.split(':', 1)[1].strip()

    return {
        'event_id': uid,
        'classroom_id': classroom_id,
        'ue_name': ue_name,
        'teacher': teacher_list,
        'class_group': class_group_list,
        'date_update': date_update,
        'date_start': dtstart,
        'date_end': dtend,
        'type': event_type
    }

def updateClassroomEvents():
    # Connexion à PostgreSQL avec psycopg3
    conn = psycopg.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )
    with conn.cursor() as cur:
        # 1. Récupérer toutes les salles et liens
        cur.execute("SELECT classroom_id, link FROM classroom_fetch_links")
        classrooms = cur.fetchall()
        if not classrooms:
            print("Aucune salle trouvée dans la base de données.")
            return

        for classroom_id, link in classrooms:
            print(f"Fetching for classroom: {classroom_id}")

            # 2. Télécharger le .ics
            resp = requests.get(link)
            if resp.status_code != 200:
                print(f"Erreur pour {classroom_id}: {resp.status_code}")
                continue

            cal = Calendar.from_ical(resp.text)

            events = []
            for component in cal.walk():
                if component.name == "VEVENT" and not component.get('UID').startswith("Ferie-"):
                    event_data = parse_event(component, classroom_id)
                    events.append(event_data)

            cur.executemany("""
                INSERT INTO classroom_events (
                    event_id, classroom_id, ue_name, teacher, class_group,
                    date_update, date_start, date_end, type
                ) VALUES (
                    %(event_id)s, %(classroom_id)s, %(ue_name)s, %(teacher)s, %(class_group)s,
                    %(date_update)s, %(date_start)s, %(date_end)s, %(type)s
                )
                ON CONFLICT (event_id) DO UPDATE SET
                    classroom_id = EXCLUDED.classroom_id,
                    ue_name = EXCLUDED.ue_name,
                    teacher = EXCLUDED.teacher,
                    class_group = EXCLUDED.class_group,
                    date_update = EXCLUDED.date_update,
                    date_start = EXCLUDED.date_start,
                    date_end = EXCLUDED.date_end,
                    type = EXCLUDED.type
            """, events)

            conn.commit()

            print(f"Terminé pour {classroom_id}")

if __name__ == "__main__":
    updateClassroomEvents()