FROM python
LABEL maintainer "Marlon francisco"

ENV PYTHONUNBUFFERED 1
RUN pip install redis

CMD ["python", "./worker.py"]