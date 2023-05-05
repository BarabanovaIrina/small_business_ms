#!/bin/sh

docker-compose -f small_business_ms/warehouse/docker-compose.yml up --build -d
docker-compose -f small_business_ms/sales/docker-compose.yml up --build -d
docker-compose -f small_business_ms/accounting/docker-compose.yml up --build -d
