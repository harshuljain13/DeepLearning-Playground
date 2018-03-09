Run Instructions
================

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd webapp
$ python manage.py runserver


$ screen -S redis-server
redis-server

$ screen -S celery-beat
cd webapp
celery -A webapp beat -l info

$ screen -S celery-worker
cd webapp
celery -A webapp worker -l info
```

