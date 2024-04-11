FROM python:3.11-slim-buster as builder

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common \
    gcc

RUN python -m venv /app/venv

COPY requirements.txt ./requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r ./requirements.txt

#used multistage for better caching and light weight image
FROM python:3.11-slim-buster 

# create user
RUN addgroup --gid 1500 user \
    && adduser --uid 1500 --gid 1500 --disabled-password user --home /home/user

RUN apt-get update && apt-get install --no-install-recommends -y \
    dumb-init \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=user:user . /home/user/app
COPY --from=builder --chown=user:user /app/venv /home/user/app/venv

ENV PATH="/home/user/app/venv/bin:$PATH"

WORKDIR /home/user/app

USER user

ENTRYPOINT [ "dumb-init", "--" ]
CMD ["python3", "app.py"]