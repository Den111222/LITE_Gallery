FROM python:3.11

ARG WD=/opt/files
ARG GROUP=files
ARG USER=fastapi

WORKDIR $WD

ENV PYTHONPATH 'src/'

RUN groupadd -r $GROUP \
    && useradd -d $WD -r -g $GROUP $USER \
    && chown $USER:$GROUP -R $WD \
    && chown $USER:$GROUP /var/log

COPY --chown=$USER:$GROUP requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

RUN apt-get update \
    && apt-get -y install gettext \
    && apt-get -y install netcat-traditional

COPY --chown=$USER:$GROUP ./src /opt/files/src
COPY --chown=$USER:$GROUP entrypoint.sh /opt/files/entrypoint.sh
COPY --chown=$USER:$GROUP main.py /opt/files/main.py
COPY --chown=$USER:$GROUP templates /opt/files/templates

EXPOSE 8080

ENTRYPOINT ["/opt/files/entrypoint.sh", "files_pg", "5432"]