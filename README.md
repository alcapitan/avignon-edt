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
sudo chmod +x app.sh
sudo cp systemd-service /etc/systemd/system/avignon-edt.service
sudo systemctl daemon-reload
sudo systemctl enable avignon-edt.service
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
0 19 * 1-5,9-12 1-5 python3 /absolute/path/to/update_classroom_events.sh >/absolute/path/to/logs.txt 2>&1
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

To make requests to the API, use the following command:

```bash
# On running locally
curl http://localhost:5000/api/events?classroom=&ue=&group=&date=
# On the official server
curl https://avignon-edt.alcapitan.me/api/events?classroom=&ue=&group=&date=
```

The date parameter is in the format `YYYY-MM-DD`, and the other parameters must exactly match the values in the `classroom_events` table.

To debug the systemd service, use the following command:

```bash
sudo journalctl -u avignon-edt.service
```
