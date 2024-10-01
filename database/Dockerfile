FROM postgres:16-alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

COPY setup_db.dev.sh /docker-entrypoint-initdb.d/

RUN ["chmod", "+x", "/docker-entrypoint-initdb.d/setup_db.dev.sh"]

EXPOSE 5432
