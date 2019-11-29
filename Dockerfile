FROM python:3.8.0
MAINTAINER Zech Zimmerman "hi@zech.codes"
WORKDIR /usr/src/app

COPY zechcodes/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY zechcodes/zechcodes zechcodes

CMD ["python3", "-m", "zechcodes"]
