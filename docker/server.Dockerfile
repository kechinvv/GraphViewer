FROM python

COPY server server
WORKDIR /server

RUN pip install -r requirements.txtsl 
ENTRYPOINT ["python", "./app.py"]