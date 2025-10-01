from __future__ import annotations
from typing import Iterable, List, Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .models import Base, Company, OKRCycle, Objective, KeyResult, KRUpdate
from ..config.settings import settings

_engine = create_engine(settings.db_url, echo=False)
Base.metadata.create_all(_engine)


def get_session() -> Session:
    return Session(_engine)

# Companies

def upsert_company(name: str) -> Company:
    with get_session() as s:
        comp = s.scalars(select(Company).where(Company.name == name)).first()
        if comp:
            return comp
        comp = Company(name=name)
        s.add(comp)
        s.commit()
        s.refresh(comp)
        return comp

# Cycles/Objectives/KRs

def create_cycle(company_id: int, name: str, start_date, end_date) -> OKRCycle:
    with get_session() as s:
        cycle = OKRCycle(company_id=company_id, name=name, start_date=start_date, end_date=end_date)
        s.add(cycle)
        s.commit()
        s.refresh(cycle)
        return cycle


def create_objective(cycle_id: int, owner: str, text: str) -> Objective:
    with get_session() as s:
        obj = Objective(cycle_id=cycle_id, owner=owner, text=text)
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj


def add_kr(objective_id: int, text: str, target: float | None = None, unit: str | None = None) -> KeyResult:
    with get_session() as s:
        kr = KeyResult(objective_id=objective_id, text=text, target=target, unit=unit)
        s.add(kr)
        s.commit()
        s.refresh(kr)
        return kr


def list_objectives(cycle_id: int) -> List[Objective]:
    with get_session() as s:
        return list(s.query(Objective).filter_by(cycle_id=cycle_id).all())


def list_krs(objective_id: int) -> List[KeyResult]:
    with get_session() as s:
        return list(s.query(KeyResult).filter_by(objective_id=objective_id).all())


def add_kr_update(kr_id: int, note: str, progress: float | None = None) -> KRUpdate:
    with get_session() as s:
        upd = KRUpdate(kr_id=kr_id, note=note, progress=progress)
        s.add(upd)
        s.commit()
        s.refresh(upd)
        return upd
