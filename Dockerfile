FROM python:3.9.4
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
WORKDIR /mysite
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
