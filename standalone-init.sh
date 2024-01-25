#!/bin/bash

MONGO_INITDB_ROOT_USERNAME=rootusr
MONGO_INITDB_ROOT_PASSWORD=rootpwd
MONGO_USER_USERNAME=rwuser
MONGO_USER_PASSWORD=rwpwd
CONTAINER_NAME=mongodb-node-4

docker exec $CONTAINER_NAME mongosh --quiet --eval 'rs.initiate()'

docker exec $CONTAINER_NAME mongosh --quiet \
    --eval 'use admin' \
    --eval "db.createUser({user: '$MONGO_INITDB_ROOT_USERNAME', pwd: '$MONGO_INITDB_ROOT_PASSWORD',roles:[{role: 'root',db:'admin'}]});"
docker exec $CONTAINER_NAME mongosh --quiet \
    --eval 'use admin' \
    --eval "db.auth('$MONGO_INITDB_ROOT_USERNAME','$MONGO_INITDB_ROOT_PASSWORD')" \
    --eval "db.createUser({user: '$MONGO_USER_USERNAME',pwd: '$MONGO_USER_PASSWORD',roles:[{role: 'readWrite',db: 'shopping_cart'}]});"