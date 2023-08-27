FROM python:3.8
WORKDIR /app/
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN python3.8 init_db.py
CMD ["python3.8", "app.py"]
EXPOSE 3111
