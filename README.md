# nychealth

This project sets up an API serving NYC restaurant health inspection data as well as a simple frontend to query it.

There are two primary components:

- Script that loads a local snapshot of the city's restaurant inspection data dump into PostgreSQL.
- A Flask app that serves both the API and the website.

## Dependencies

```
pip install -r requirements.txt
```

# Running

## Configuration

The file `credentials.sample` is provided as a template for you to provide necessary credentials to both load and read the database. You should have a copy of this file with your desired credentials filled in, and the `$NYCHEALTH_CREDENTIALS` env var should point to this file.

Do not check this file into source control with actual data, and consider not filling in the `SQL_WRITE_USER` and `SQL_WRITE_PASSWORD` fields when deploying to the web.

## Loading Data

Before we get too far, we need to load the restaurant inspection results in CSV format into a database. I'm using PostgreSQL.

Restaurant inspection datasets get updated infrequently, but you may want to set up a cron job to pull the latest and rebuild the database. Note that the webserver does not need credentials to write to the database, so it's best to leave those blank. Only the machine updating the database (maybe your own box, maybe a deploy box, maybe something else) needs the write-access credentials.

1. Download a copy of [the DOHMH NYC Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/) in CSV format (hit 'Export').
2. `TODO`

## Debug/Development (Webserver)

1. Install all dependencies
3. `python nychealth.py` to launch debug webserver

## Deployment (Webserver)

I host this on EC2, so the instructions here will be EC2-centric but should be applicable with minor modifications elsewhere.

1. SSH onto your webserver.
2. Install all dependencies.
3. Set up apache and install mod_wsgi.
4. Check the codebase out into Apache's webpath (or symlink it, whatever).
5. Futz with your config and VirtualHosts to get the WSGI app running - [consult this blog post as an example](http://alex.nisnevich.com/blog/2014/10/01/setting_up_flask_on_ec2.html).
6. Make sure your credentials are configured correctly to connect to the database.
7. Bounce the server and off you go!
