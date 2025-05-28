# Avignon-EDT API

Attention, this project is not official and does not have any affiliation with the University of Avignon.  
It is a personal project created strictly for personal use.

## Installation

Set up a PostgreSQL on your server and create a database named `avignon-edt`, then run the following command to initialize the database with its tables and data:

```bash
psql -h your-server.com -U your-user -d avignon-edt -f init_db_psql.sql
```

Next, set up the project by installing the environment and dependencies. You can do this by running the following commands:

```bash
sudo apt install python3 python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo chmod +x update_classroom_events.sh
sudo chmod +x avignon-edt
sudo cp systemd-service /etc/systemd/system/avignon-edt.service
sudo systemctl daemon-reload
sudo systemctl enable avignon-edt.service
sudo systemctl start avignon-edt.service
sudo cp nginx-config /etc/nginx/sites-available/avignon-edt
sudo ln -s /etc/nginx/sites-available/avignon-edt /etc/nginx/sites-enabled/avignon-edt
sudo systemctl restart nginx
```

Then, create a `.env` file in the root directory of the project and add the following variables:

```env
PGHOST=your-server.com
PGPORT=5432
PGDATABASE=avignon-edt
PGUSER=your-user
PGPASSWORD=your-password
```

Finally, make the classroom events table up to date by running the following command every day at 19:00, from Monday to Friday, from September to December and from January to May :

```bash
0 19 * 1-5,9-12 1-5 /absolute/path/to/update_classroom_events.sh >/absolute/path/to/logs.txt 2>&1
```

## Usage

To fill the `classroom_events` table with the data from the APIs listed in `classroom_fetch_links` table, run the following command:

```bash
./update_classroom_events.sh
```

To run the API, use the following command:

```bash
./avignon-edt
```

To debug the systemd service, use the following command:

```bash
sudo journalctl -u avignon-edt.service
```

### Search for events

Here is the API endpoint to search for events:

```http
GET /api/events?classroom=&ue=&group=&date=
```

The parameters `classroom`, `ue`, `group`, and `date` are optional. If you do not provide any parameters, it will return all events. If you provide a parameter, it will filter the results based on that parameter.  
The `date` parameter in the URL must be in the format `YYYY-MM-DD`, but in the data from the API, the date format is ISO 8601.

### List elements

Here are the API endpoints to list elements:

```http
GET /api/list/ue
GET /api/list/classroom
GET /api/list/group
GET /api/list/teacher
```

There return a list of all unique elements in the `classroom_events` table for the specified type.
