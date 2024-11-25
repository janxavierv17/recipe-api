# Dockerfile definitions for our os level dependendies.
FROM python:3.9-alpine3.13
LABEL maintainer="Jan"

# Recommended to have when running python on a docker container
# Ensures stdout & stderr streams are sent straight to terminal(container log) and in real time.
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# To override in our docker-compose.yml
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    echo -e "\033[1;33m=== Development mode enabled. Installing development dependencies... ===\033[0m"; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

# Commands will run as django-user rather than root
USER django-user