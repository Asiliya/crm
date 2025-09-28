FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /crm_app

COPY . /crm_app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod a+x /crm_app/crm/entrypoint.sh

EXPOSE 8000

CMD ["sh", "crm/entrypoint.sh"]
