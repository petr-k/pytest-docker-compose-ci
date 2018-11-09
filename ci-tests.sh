#!/usr/bin/env bash

docker-compose \
  -f ci-docker-compose-tests.yml \
  -f tests/docker-compose.yml \
  up \
  --force-recreate \
  --build \
  --exit-code-from app

EXIT_CODE=$?

docker-compose \
  -f ci-docker-compose-tests.yml \
  -f tests/docker-compose.yml \
  down \
  --volumes \
  --rmi local

exit $EXIT_CODE
