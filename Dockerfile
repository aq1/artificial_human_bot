FROM python:3.10-bullseye

USER django

ENV PATH="/home/django/.local/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY --chown=django:django requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=django:django ./main.py .

CMD python main.py
