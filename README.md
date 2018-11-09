# pytest-docker-compose-ci

## Run tests using local Python

* Create a virtual env, switch to it
* Install requirements in `requirements-dev.txt`
* Run `pytest`. This will bring up test-time dependencies using
  `docker-compose` and tear down appropriately.

## Run tests in a CI environment
* Run `ci-tests.sh`. Only `docker` and `docker-compose` is required.

