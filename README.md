# Transparansi

A financial transparency platform built as a proof of concept for how a simple,
accountable ledger can create visibility into how money moves — and make corruption
harder to hide.

Anyone can observe. Only authorized people can touch the money.

---

## The Problem
In large organizations — governments, institutions, even businesses — money disappears
not because systems are complex, but because they're opaque. No one can see where it
went, who approved it, or whether it was legitimate. Transparansi is a simple answer
to that: make every transaction visible, every approval traceable, every bill
accountable.

---

## Features
- **Role-based access** — Admin, Supervisor, Staff, and public Observers
- **Project budgeting** — Allocate funds from a central wallet to individual projects
- **Task management** — Break projects into tasks and subtasks, assign staff
- **Bill workflow** — Staff submits bills, supervisors approve or reject
- **Immutable ledger** — No deletions, every transaction is permanent, refunds create new entries
- **Full audit trail** — Every change on every record is logged
- **Public observer view** — No account needed to see where money is going

---

## Tech Stack
- **FastAPI** — Web framework
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **PostgreSQL** — Database
- **Pydantic** — Data validation
- **JWT** — Authentication

---

## Project Status
🚧 In active development — MVP in progress

---

## Setup
_Coming soon_

---

## Design
See [DESIGN.md](./DESIGN.md) for full system design, data models, and flows.
