FROM python:3.9.4
ENV PYTHONUNBUFFERED 1
WORKDIR /mysite
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3.9","manage.py","runserver","0.0.0.0:8000"]