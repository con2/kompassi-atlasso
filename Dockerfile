FROM python:2.7
WORKDIR /usr/src/app
COPY requirements.txt requirements-production.txt /usr/src/app/
RUN groupadd -r atlasso && useradd -r -g atlasso atlasso && \
    pip install --no-cache-dir -r requirements.txt -r requirements-production.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q .
USER atlasso
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
