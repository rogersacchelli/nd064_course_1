FROM python:3.8
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN python3.8 init_db.py
CMD ["python3.8", "app.py"]
EXPOSE 3111
