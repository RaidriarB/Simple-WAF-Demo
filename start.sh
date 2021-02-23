source .venv/bin/activate

cd src
nohup python3 main.py &

cd ../src_frontend
python3 manage.py runserver 0.0.0.0:8080