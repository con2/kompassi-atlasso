FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN groupadd -r atlasso && useradd -r -g atlasso atlasso && \
    pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
USER atlasso
EXPOSE 8000
ENV PYTHONUNBUFFERED=1

# NOTE: if increasing --workers, switch from in-memory sqlite to a real database
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0", "--access-logfile=-", "--capture-output", "atlasso.wsgi"]
