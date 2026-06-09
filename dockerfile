FROM python:3.9.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

#Enable BuildKit and use cache to stop Docker from reinstalling node_modules every time and reuse cache
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "GH.wsgi:application"]