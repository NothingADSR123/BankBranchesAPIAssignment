# Bank Branches API

A clean REST API built using FastAPI that provides bank and branch details. The data is loaded from a CSV file into a SQLite database on application startup.

🔗 Live API (Deployed on Render):
https://bankbranchesapiassignment.onrender.com/

Overview
Provides APIs to:
List all banks
Fetch branch details using IFSC
On startup:
Creates database schema
Loads data from data/bank_branches.csv (only if DB is empty)
Built strictly as per assignment requirements (no external APIs or SQL dumps used)

Tech stack
- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- SQLite (local `app.db`)
- Pytest (tests)

Project layout
```
project/
├── app/
│   ├── main.py          # application, loader and startup logic
│   ├── database.py      # SQLAlchemy engine/session/base
│   ├── models.py        # ORM models (Bank, Branch)
│   ├── schemas.py       # Pydantic response models
│   └── routes.py        # API routes
├── data/bank_branches.csv
├── tests/test_api.py
├── requirements.txt
└── README.md
```

Setup (local)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python -m uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

API Endpoints
- `GET /banks` — returns an array of banks:

  Response sample:

  ```json
  [{"id": 1, "name": "ABHYUDAYA COOPERATIVE BANK LIMITED"}, ...]
  ```

- `GET /branches?ifsc=XXXX` — returns a branch object with nested `bank`:

  Response sample:

  ```json
  {
    "ifsc": "ABHY0065001",
    "branch": "RTGS-HO",
    "address": "...",
    "city": "MUMBAI",
    "district": "GREATER MUMBAI",
    "state": "MAHARASHTRA",
    "bank": {"id": 1, "name": "ABHYUDAYA COOPERATIVE BANK LIMITED"}
  }
  ```

Error handling
- `GET /branches` with an unknown IFSC responds with `404` and `{"detail":"IFSC not found"}`.

Tests
- Unit tests use FastAPI's TestClient and are located at `tests/test_api.py`.
- Run tests with:

```powershell
python -m pytest -q
```

Design notes & decisions
- Database schema follows the assignment: `banks (id, name)` and `branches (ifsc, branch, address, city, district, state, bank_id)`.
- SQLAlchemy ORM is used for models and queries.
- On startup the app creates tables and imports CSV rows. Import logic avoids duplicate banks and skips branches whose IFSC already exists.
- Pydantic schemas are provided for clean API responses.

Time taken
- ~12 hours (approx.)

Submission
- Author: Aditya Srivastava

