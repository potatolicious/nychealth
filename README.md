# nychealth

API for accessing pre-loaded NYC health inspection data.

# Requirements

This assumes you're deploying onto EC2. You may need to futz with `fabfile.py` if your configuration is different.

## Dependencies

```
pip install boto
pip install fabric
pip install Flask
pip install gunicorn
```

# Running

## Configuration

The file `credentials.sample` is provided as a template for you to provide your own AWS credentials for deployment. You should have a copy of this file with your AWS credentials, and the `$NYCHEALTH_CREDENTIALS` environment variable should contain the path to this file.

As always, don't check this file into any repo, because that just wouldn't be smart.

## Debug/Development

1. Install all dependencies
2. `python nychealth.py` to launch debug webserver

## Deployment

1. Install all dependencies.
2. `gunicorn nychealth:app -p ~/nychealth_app.pid -b 127.0.0.1:8000 -D`

## To restart

`kill -HUP \`cat ~/nychealth_app.pid\``

## To shutdown

`kill \`cat ~/nychealth_app.pid\``
