from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Date, Text, Float

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

class OKRCycle(Base):
    __tablename__ = "okr_cycles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    company: Mapped[Company] = relationship()

class Objective(Base):
    __tablename__ = "objectives"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cycle_id: Mapped[int] = mapped_column(ForeignKey("okr_cycles.id"), nullable=False)
    owner: Mapped[str] = mapped_column(String(80), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

class KeyResult(Base):
    __tablename__ = "key_results"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    objective_id: Mapped[int] = mapped_column(ForeignKey("objectives.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    target: Mapped[Optional[float]] = mapped_column(Float)
    unit: Mapped[Optional[str]] = mapped_column(String(32))
    current: Mapped[Optional[float]] = mapped_column(Float)
    confidence: Mapped[Optional[int]] = mapped_column(Integer)  # 0~100

class KRUpdate(Base):
    __tablename__ = "kr_updates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kr_id: Mapped[int] = mapped_column(ForeignKey("key_results.id"), nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    progress: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class DailyProgress(Base):
    __tablename__ = "daily_progress"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    objective_id: Mapped[int] = mapped_column(ForeignKey("objectives.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    ai_validation: Mapped[Optional[str]] = mapped_column(Text)
    ai_comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)