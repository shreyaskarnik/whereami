FROM mxnet/python:latest
COPY . /app/
WORKDIR /app
RUN pip install --upgrade -r requirements.txt
ENTRYPOINT [ "python", "app.py" ]
EXPOSE 8080