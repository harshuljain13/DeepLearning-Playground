Run Instructions
================

```
mkdir data
cd data

wget http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar
extract the tar folder and put everything inside dogs directory.

cd data
mkdir inception
Download everything related to inception model here.

cd data
Get the NIST dataset
extract the NIST dataset and rename the main directory as NIST19
```

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

