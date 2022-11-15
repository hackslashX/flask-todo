FROM python:3.8

RUN addgroup --system app && adduser --system --group app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

WORKDIR /todo/

RUN curl -sSL https://install.python-poetry.org/ | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY main/poetry.lock main/pyproject.toml /todo/
RUN poetry install --no-dev

COPY ./main/ /todo

ENV PYTHONPATH=/todo

RUN chown -R app:app $HOME

RUN chmod +x run.sh
RUN chmod +x prestart.sh