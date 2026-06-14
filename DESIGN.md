# Transparansi — System Design Document

## The Idea

A financial transparency platform — proof of concept for how a simple, accountable ledger
could reduce corruption. Anyone can observe where money goes, only authorized people can
touch it. Built around the idea that visibility alone is a form of accountability.

---

## Tech Stack

| Layer      | Tool                                        |
| ---------- | ------------------------------------------- |
| Framework  | FastAPI                                     |
| ORM        | SQLAlchemy (async)                          |
| Migrations | Alembic                                     |
| Database   | PostgreSQL                                  |
| Templating | Jinja2                                      |
| Styling    | Tailwind CSS                                |
| Validation | Pydantic (built into FastAPI)               |
| Auth       | Session-based (Starlette SessionMiddleware) |

---

## Roles & Access

| Role       | Account Needed | What They Can Do                                                   |
| ---------- | -------------- | ------------------------------------------------------------------ |
| Observer   | No             | View all projects, tasks, bills publicly                           |
| Staff      | Yes            | Submit bills, get assigned to tasks                                |
| Supervisor | Yes            | Manage assigned projects, create tasks, approve/reject bills       |
| Admin      | Yes            | Create projects, allocate budgets, assign supervisors, full access |

---

## Data Hierarchy

```
System Wallet
└── Project (budget allocated from System Wallet, assigned to 1 Supervisor)
    └── Task (can have subtasks via parentTaskID — recursive)
        └── Bill (submitted by Staff, approved/rejected by Supervisor)
```

---

## Database Tables

### users

| Field                    | Type     | Notes                                    |
| ------------------------ | -------- | ---------------------------------------- |
| id                       | UUID PK  |                                          |
| username                 | string   | unique                                   |
| password_hash            | string   |                                          |
| full_name                | string   |                                          |
| date_of_birth            | date     |                                          |
| clearance_level          | enum     | observer, staff, supervisor, admin       |
| is_active                | bool     | default true                             |
| date_joined              | datetime |                                          |
| date_left                | datetime | nullable                                 |
| session_token            | string   | nullable, unique                         |
| session_token_expires_at | datetime | nullable                                 |

---

### wallets

| Field       | Type       | Notes           |
| ----------- | ---------- | --------------- |
| id          | UUID PK    |                 |
| wallet_name | string     | unique          |
| description | string     | nullable        |
| wallet_type | enum       | system, project |
| is_active   | bool       |                 |
| created_at  | datetime   |                 |
| created_by  | FK → users |                 |

> Projects reference wallets (via `wallet_id` on the projects table), not the other way around.

---

### walletTransactions

Immutable. No deletes. Refunds/cancellations create a new entry.

| Field          | Type                      | Notes                                                                  |
| -------------- | ------------------------- | ---------------------------------------------------------------------- |
| id             | UUID PK                   |                                                                        |
| tx_name        | string                    |                                                                        |
| amount         | decimal                   |                                                                        |
| tx_type        | enum                      | deposit, allocation, bill_payment, refund, cancellation, pending       |
| from_wallet_id | FK → wallets              | nullable                                                               |
| to_wallet_id   | FK → wallets              | nullable                                                               |
| bill_id        | FK → bills                | nullable, used when tx_type = bill_payment                             |
| is_cancelled   | bool                      | default false                                                          |
| refund_id      | FK → wallet_transactions  | nullable, points to original tx if this is a refund                    |
| description    | string                    | nullable                                                               |
| created_at     | datetime                  |                                                                        |
| cancelled_at   | datetime                  | nullable                                                               |

---

### projects

| Field          | Type         | Notes                                          |
| -------------- | ------------ | ---------------------------------------------- |
| id             | PK           |                                                |
| name           | string       |                                                |
| description    | string       | nullable                                       |
| expectedBudget | decimal      | initial planned budget                         |
| status         | enum         | pending, ongoing, delayed, finished, cancelled |
| supervisorID   | FK → users   | assigned supervisor                            |
| walletID       | FK → wallets | one wallet per project                         |
| createdAt      | datetime     |                                                |
| finishedAt     | datetime     | nullable                                       |

> currentExpense is always calculated, never stored:
> `SUM of approved bill amounts where bill → task → project = this project`

---

### tasks

Recursive. A task can be a subtask by pointing parentTaskID to another task.

| Field        | Type          | Notes                                  |
| ------------ | ------------- | -------------------------------------- |
| id           | UUID PK       |                                        |
| task_name    | string        |                                        |
| description  | string        | nullable                               |
| projectID    | FK → projects |                                        |
| parentTaskID | FK → tasks    | nullable, null = top-level task        |
| status       | enum          | pending, ongoing, completed, cancelled |
| assignees    | M2M → users   | via task_assignees join table          |
| created_by   | FK → users    |                                        |
| created_at   | datetime      |                                        |
| finished_at  | datetime      | nullable                               |

---

### bills

| Field       | Type       | Notes                                                                    |
| ----------- | ---------- | ------------------------------------------------------------------------ |
| id          | UUID PK    |                                                                          |
| bill_name   | string     |                                                                          |
| amount      | decimal    |                                                                          |
| task_id     | FK → tasks | bills attach to tasks, not projects directly                             |
| submittedBy | FK → users | staff who submitted                                                      |
| status      | enum       | pending, approved, rejected, cancelled                                   |
| approved_by | FK → users | nullable, supervisor who approved/rejected                               |
| description | string     | nullable                                                                 |
| created_at  | datetime   |                                                                          |
| resolved_at | datetime   | nullable                                                                 |

> wallet_transactions link back to bills via `bill_id` FK on wallet_transactions (not a join table).

---

### changes (audit log)

> **Not yet implemented.** Planned — tracks modifications on any record.

| Field        | Type       | Notes                     |
| ------------ | ---------- | ------------------------- |
| id           | PK         |                           |
| tableName    | string     | e.g. "bills", "projects"  |
| recordID     | int/UUID   | ID of the modified record |
| changedBy    | FK → users |                           |
| changedAt    | datetime   |                           |
| fieldChanged | string     | e.g. "status"             |
| oldValue     | string     | serialized old value      |
| newValue     | string     | serialized new value      |

---

## Core Flows

### 1. Budget Allocation

1. Admin deposits funds into System Wallet (walletTransaction: type=deposit)
2. Admin creates Project, allocates budget from System Wallet to Project Wallet (walletTransaction: type=allocation)

### 2. Bill Submission & Approval

1. Supervisor creates Task under Project, assigns Staff
2. Staff submits Bill under a Task (status: pending)
3. Supervisor reviews → approves or rejects
4. On approval → walletTransaction created (type=bill_payment), deducted from Project Wallet
5. On rejection → bill status = rejected, no transaction created

### 3. Public Observation

- Anyone can view all projects, their budgets, tasks, and approved bills
- No account needed

---

## MVP Scope

Get this full flow working end to end before adding anything else:

- [x] Auth (session-based, role-based) — 2026-05-20
- [x] Create wallet (system or project type) — 2026-06-01
- [x] Create project (linked to a wallet) — 2026-06-14
- [ ] System wallet deposit (walletTransaction type=deposit)
- [ ] Budget allocation from system wallet to project wallet (walletTransaction type=allocation)
- [ ] Wallet info page with ledger and calculated funds — in progress
- [ ] Create tasks + subtasks
- [ ] Submit bill
- [ ] Approve/reject bill → wallet deduction
- [ ] Public observer endpoints

---

## Future Features (post-MVP)

- Recurring bills
- Email notifications on approval/rejection
- Export reports (PDF)
- Staff ↔ Supervisor linking table
- Dashboard analytics
