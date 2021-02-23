source .venv/bin/activate


cd src_frontend
nohup python3 manage.py runserver 0.0.0.0:8080 &

cd ../src
python3 main.py