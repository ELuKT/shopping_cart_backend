#!/bin/bash

until curl -s -f ${CONSUL_HTTP_ADDR}/v1/status/leader | grep 8300; do
  echo "Waiting for Consul to start"
  sleep 1
done

if [ ! -z "$SERVICE_CONFIG" ]; then
  echo "Registering service with consul $SERVICE_CONFIG"
  # https://docs.aws.amazon.com/AmazonECS/latest/userguide/task-metadata-endpoint-v4-fargate.html
  # jq default output contains quotes, -raw-output(-r) remove quotes
  address=$(curl -s ${ECS_CONTAINER_METADATA_URI_V4}/task | jq -r '.Containers[0].Networks[0].IPv4Addresses[0]')
  
  mkdir -p ${SERVICE_CONFIG%/*}
  touch ${SERVICE_CONFIG} 
  echo "{
  \"services\": [
    {
      \"id\": \"$APP_NAME\",
      \"name\": \"$SERVICE_NAME\",
      \"address\": \"$address\",
      \"port\": $APP_PORT,
      \"check\": {
        \"tcp\": \"$address:$APP_PORT\",
        \"interval\": \"10s\"
      },
      \"connect\": {
        \"sidecar_service\": {
          \"port\":19001,
          \"checks\": [
            {
              \"name\": \"Connect Sidecar Listening\",
              \"tcp\": \"$address:19001\",
              \"interval\": \"10s\"
            } 
          ]
        }
      }
    }
  ]
}
">$SERVICE_CONFIG

    if [ ! -z ${UPSTREAM_SERVICE_NAME} ]; then
      echo $(cat $SERVICE_CONFIG | jq ".services[0].connect.sidecar_service += {\"proxy\": {\"upstreams\": [{\"destination_name\": \"${UPSTREAM_SERVICE_NAME}\",\"local_bind_port\": ${UPSTREAM_BIND_PORT}}]}}") > $SERVICE_CONFIG
    fi

    if [ ! -z ${NODE_NAME} ]; then
      echo $(cat $SERVICE_CONFIG | jq ". += {\"node_name\": \"${NODE_NAME}\"}") > $SERVICE_CONFIG
    fi
    cat $SERVICE_CONFIG
    consul services register ${SERVICE_CONFIG} 

    exit_status=$? 
    if [ $exit_status -ne 0 ]; then
        exit 1
    fi

    trap "consul services deregister ${SERVICE_CONFIG}" SIGINT SIGTERM EXIT
fi

if [ "$#" -ne 0 ]; then
    echo "Running command: $@"
    exec "$@" &
    tail -f /dev/null &
    PID=$!
    wait $PID
fi
