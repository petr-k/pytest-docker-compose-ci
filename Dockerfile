FROM python:3.6

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /usr/src/app
COPY requirements*.txt ./
RUN pip install \
    --no-cache-dir \
    -r ${REQUIREMENTS_FILE}

COPY . .

CMD ["python", "main.py"]
