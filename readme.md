# startup project locally

## prerequisite
- python 3.8.16
- poetry
- create 2 google api project
    - one for oauth login, one for sending email 
    - get client id and client secret from both project

## install dependencies

run command 
```
poetry install
```

## create rsa private key and public jwks

run rsa.py to generate private key and public jwks

## use .env.template to create .env

    - GMAIL_USER: your email address
    - GMAIL_REFRESH_TOKEN: refresh access token with correct scopes
    - REDIS_PASSWORD: leave value empty 

## startup mongodb

docker compose -f docker-compose-mongodb-staodalone.yml up -d

## startup redis

docker compose -f docker-compose-redis.yml up -d

## startup backend

uvicorn app.app:app --log-config log-config.ini
