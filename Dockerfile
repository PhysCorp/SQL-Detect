FROM python:3.8-slim
WORKDIR /flaskapp
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
COPY . /flaskapp
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --force-reinstall charset-normalizer
EXPOSE 80
CMD ["python3", "main.py"]