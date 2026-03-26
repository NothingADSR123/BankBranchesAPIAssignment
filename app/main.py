from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
import csv
import os

from .database import engine, Base, get_db
from . import models, routes

# Ensure tables exist at import time so TestClient and tests don't hit missing tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routes.router)


def _load_csv_if_empty():
    db = next(get_db())
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "bank_branches.csv")
        if not os.path.exists(csv_path):
            return

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader]

            # Map existing banks
            existing_banks = {b.name: b.id for b in db.query(models.Bank).all()}

            # Ensure all banks exist
            for r in rows:
                name = (r.get('bank_name') or '').strip()
                if not name:
                    continue
                if name not in existing_banks:
                    b = models.Bank(name=name)
                    db.add(b)
                    db.commit()
                    existing_banks[b.name] = b.id

            # Insert branches if IFSC not present
            for r in rows:
                ifsc = (r.get('ifsc') or r.get('IFSC') or '').strip()
                if not ifsc:
                    continue
                exists = db.query(models.Branch).filter(models.Branch.ifsc == ifsc).first()
                if exists:
                    continue
                bank_id = existing_banks.get((r.get('bank_name') or '').strip())
                if not bank_id:
                    continue
                branch = models.Branch(
                    ifsc=ifsc,
                    branch=(r.get('branch') or r.get('BRANCH') or '').strip(),
                    address=(r.get('address') or '').strip(),
                    city=(r.get('city') or '').strip(),
                    district=(r.get('district') or '').strip(),
                    state=(r.get('state') or '').strip(),
                    bank_id=bank_id,
                )
                db.add(branch)
            db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    _load_csv_if_empty()


# Load immediately at import so tests and TestClient see data
_load_csv_if_empty()
