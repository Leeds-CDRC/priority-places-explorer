FROM python:3.9-slim

COPY data /data
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

ENTRYPOINT [ "python" ]
CMD ["application.py"]
