#!/bin/sh

docker-compose -f small_business_ms/warehouse/docker-compose.yml build
docker-compose -f small_business_ms/sales/docker-compose.yml build
docker-compose -f small_business_ms/accounting/docker-compose.yml build
