#  Fleek Image Generator – Async FastAPI + Celery + Redis + PostgreSQL

This is a fullstack backend task assignment for Fleek, showcasing a production-ready image generation API using:

- **FastAPI** for the async REST API
- **PostgreSQL** for job persistence
- **Celery** for async task processing
- **Redis** as the message broker
- **SQLModel** for DB models (Pydantic + SQLAlchemy)
- **System Design** with full separation of concerns

---

##  Features

- Submit a prompt and generate an image file (simulated as `.txt`)
- Asynchronous background processing via Celery worker
- Job status tracking (`pending`, `completed`, `failed`)
- Result path + error info stored in the database
- End-to-end decoupled architecture (API doesn't block)

---

##  Project Structure

fleek-assignment
├── README.md
├── backend
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── main.cpython-310.pyc
│   │   └── main.cpython-313.pyc
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── routes.cpython-310.pyc
│   │   │   └── routes.cpython-313.pyc
│   │   └── routes.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── celery_app.cpython-310.pyc
│   │   │   ├── celery_app.cpython-313.pyc
│   │   │   ├── db.cpython-310.pyc
│   │   │   └── db.cpython-313.pyc
│   │   ├── celery_app.py
│   │   └── db.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── job.cpython-310.pyc
│   │   │   └── job.cpython-313.pyc
│   │   └── job.py
│   ├── requirements.txt
│   ├── services
│   │   ├── __init__.py
│   │   └── replicate_service.py
│   └── tasks
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-310.pyc
│       │   ├── __init__.cpython-313.pyc
│       │   ├── worker.cpython-310.pyc
│       │   └── worker.cpython-313.pyc
│       └── worker.py
└── results


---

## 🧪 How to Run (Dev Environment)

### 1.  Start PostgreSQL locally
Make sure PostgreSQL is running locally:

❯ pg_ctl -D /Library/PostgreSQL/15/data start

2.  Start Redis server
# For example (macOS):
brew services start redis

3.  Create virtualenv + install deps
python3 -m venv fleek-assignment-venv
source fleek-assignment-venv/bin/activate

pip install -r backend/requirements.txt

4.  Apply DB migrations (table creation)
# inside FastAPI app
cd backend
python -c 'import asyncio; from backend.core.db import init_db; asyncio.run(init_db())'

## Running the System
A. Start FastAPI (dev)
uvicorn backend.main:app --reload
B. Start Celery Worker (in separate terminal)
celery -A backend.core.celery_app.celery_app worker --loglevel=info -Q default

## API Endpoints
1. Submit image generation job

POST /generate
Content-Type: application/json

Payload:
{
  "prompt": "a ninja drinking coffee",
  "parameters": {
    "width": 512,
    "height": 512
  }
}

Response:
{
  "job_id": "9b215c56-595d-4548-9528-a26019ba1ffc"
}

2. Check job status

GET /status/{job_id}
Example:
curl http://127.0.0.1:8000/status/9b215c56-595d-4548-9528-a26019ba1ffc

Response:
{
  "job_id": "9b215c56-595d-4548-9528-a26019ba1ffc",
  "status": "completed",
  "result": "results/9b215c56-595d-4548-9528-a26019ba1ffc.txt",
  "error": null
}

🧠 How It Works
User submits prompt via /generate

FastAPI creates a Job record in Postgres with pending status

Celery picks it up from Redis broker

Worker writes result_path file and updates the DB to completed

Frontend (or API) polls /status/{job_id} to show results

## Example Output File
Path: results/9b215c56-595d-4548-9528-a26019ba1ffc.txt
Generated: a ninja drinking coffee with {'width': 512, 'height': 512}

 Tech Stack

 | Layer          | Tech                    |
| -------------- | ------------------------ |
| API            | FastAPI                  |
| Async DB       | SQLModel + asyncpg       |
| Sync DB (task) | SQLAlchemy ORM           |
| Tasks          | Celery                   |
| Broker         | Redis                    |
| DB             | PostgreSQL               |
| Worker Queue   | Celery with `-Q default` |

Cleanup
All generated files are written under /results/
No actual image generation – simulated for task
Fully decoupled for real-world extension (e.g. pass to model)

 Author
Christyan Simbolon

GitHub: @chrisimbolon
Email: christyansimbolon@gmail.com
Assignment submitted for Fleek – 25 July 2025

Notes
Project runs fully offline

No Docker used in this version to keep setup transparent

Ready for deployment via Gunicorn/Uvicorn + Flower if needed