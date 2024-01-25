# docker build -t aws-consul-envoy:0.1.0 -f Dockerfile .
FROM hashicorp/consul:1.16.2 as consul-bin
FROM envoyproxy/envoy:v1.26.6 as envoy-bin

FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
    jq \
    curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=envoy-bin /usr/local/bin/envoy /bin/envoy

COPY --from=consul-bin /bin/consul /bin/consul

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]