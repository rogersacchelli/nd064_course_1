FROM python:3.8
COPY . /app
WORKDIR /app
RUN ls
RUN pip install -r requirements.txt
RUN python3.8 init_db.py
CMD ["python3.8", "app.py"]
EXPOSE 3111
