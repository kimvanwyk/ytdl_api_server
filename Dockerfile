FROM registry.gitlab.com/kimvanwyk/fastapi-poetry

COPY ./ytdl_api_server/*.py /app/

ENV DB_FILE_PATH=/db/db.sqlite3
