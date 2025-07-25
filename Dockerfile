FROM python:3.11-slim

WORKDIR /app
COPY ./backend /app/backend
COPY ./backend/requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
