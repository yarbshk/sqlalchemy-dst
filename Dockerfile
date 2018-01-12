FROM python:3.5-jessie

ENV PYTHONPATH="${PROJECT_ROOT}sqlalchemy_dst:${PYTHONPATH}"

ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm -f /tmp/requirements.txt
