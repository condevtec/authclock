FROM python:3.6-alpine as base

# *** Deploy Stage ***
FROM base as deploy

RUN mkdir /app && chown nobody:nobody /app

# *** Backend Stage ***
FROM base as backend

RUN apk add --update --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    tzdata


RUN mkdir -p /app/logs

# python requirements
ADD ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt --upgrade --no-cache-dir

# copy pyproject file

WORKDIR /app
COPY ./app/ /app/app

# *** Deploy Stage ***
FROM deploy

EXPOSE 5000
ENV FLASK_ENV=production

WORKDIR /app

COPY --from=backend --chown=nobody:nobody /app /app

USER nobody
CMD CPUS=$(grep -c processor /proc/cpuinfo) \
    gunicorn \
    --access-logfile - \
    --error-logfile - \
    --workers {{ CPUS }} \
    --worker-class gevent \
    --worker-connections=1000 \
    --keep-alive 3 \
    --max-requests=10000 \
    --timeout 30 \
    --graceful-timeout 30 \
    --bind 0.0.0.0:5000 \
    --reload app:app
