# Transparansi — System Design Document

## The Idea
A financial transparency platform — proof of concept for how a simple, accountable ledger
could reduce corruption. Anyone can observe where money goes, only authorized people can
touch it. Built around the idea that visibility alone is a form of accountability.

---

## Tech Stack
| Layer | Tool |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL |
| Validation | Pydantic (built into FastAPI) |
| Auth | Session-based (Starlette SessionMiddleware) |

---

## Roles & Access

| Role | Account Needed | What They Can Do |
|---|---|---|
| Observer | No | View all projects, tasks, bills publicly |
| Staff | Yes | Submit bills, get assigned to tasks |
| Supervisor | Yes | Manage assigned projects, create tasks, approve/reject bills |
| Admin | Yes | Create projects, allocate budgets, assign supervisors, full access |

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
| Field | Type | Notes |
|---|---|---|
| id | UUID/int PK | |
| username | string | unique |
| passwordHash | string | |
| fullName | string | |
| dateOfBirth | date | |
| clearanceLevel | enum | observer, staff, supervisor, admin |
| employeeID | string | unique |
| isActive | bool | default true |
| dateJoined | datetime | |
| dateLeft | datetime | nullable |

---

### wallets
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | |
| description | string | nullable |
| type | enum | system, project |
| projectID | FK → projects | nullable, null = system wallet |
| isActive | bool | |
| createdAt | datetime | |
| createdBy | FK → users | |

---

### walletTransactions
Immutable. No deletes. Refunds/cancellations create a new entry.

| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | |
| amount | decimal | |
| type | enum | deposit, allocation, bill_payment, refund, cancellation |
| fromWalletID | FK → wallets | nullable |
| toWalletID | FK → wallets | nullable |
| billID | FK → bills | nullable, used when type = bill_payment |
| isCancelled | bool | default false |
| refundID | FK → walletTransactions | nullable, points to original tx if this is a refund |
| description | string | nullable |
| createdAt | datetime | |
| cancelledAt | datetime | nullable |

---

### projects
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | |
| description | string | nullable |
| expectedBudget | decimal | initial planned budget |
| status | enum | pending, ongoing, delayed, finished, cancelled |
| supervisorID | FK → users | assigned supervisor |
| walletID | FK → wallets | one wallet per project |
| createdAt | datetime | |
| finishedAt | datetime | nullable |

> currentExpense is always calculated, never stored:
> `SUM of approved bill amounts where bill → task → project = this project`

---

### tasks
Recursive. A task can be a subtask by pointing parentTaskID to another task.

| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | |
| description | string | nullable |
| projectID | FK → projects | |
| parentTaskID | FK → tasks | nullable, null = top-level task |
| status | enum | pending, ongoing, completed, cancelled |
| assignees | M2M → users | staff assigned to this task |
| createdAt | datetime | |
| finishedAt | datetime | nullable |

---

### bills
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | |
| amount | decimal | |
| taskID | FK → tasks | bills attach to tasks, not projects directly |
| submittedBy | FK → users | staff who submitted |
| status | enum | pending, approved, rejected, cancelled |
| approvedBy | FK → users | nullable, supervisor who approved/rejected |
| transactionIDs | M2M → walletTransactions | supports partial payments |
| description | string | nullable |
| createdAt | datetime | |
| resolvedAt | datetime | nullable |

---

### changes (audit log)
Tracks modifications on any record. Linked records store a list of change IDs.

| Field | Type | Notes |
|---|---|---|
| id | PK | |
| tableName | string | e.g. "bills", "projects" |
| recordID | int/UUID | ID of the modified record |
| changedBy | FK → users | |
| changedAt | datetime | |
| fieldChanged | string | e.g. "status" |
| oldValue | string | serialized old value |
| newValue | string | serialized new value |

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
- [ ] Auth (session-based, role-based)
- [ ] System wallet + deposit
- [ ] Create project + allocate budget
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
