-- library for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


DROP TYPE IF EXISTS clearance_level;
CREATE TYPE clearance_level AS ENUM ('observer', 'staff', 'supervisor', 'admin');

-- now only users table
CREATE TABLE IF NOT EXISTS users (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    username        VARCHAR(100) NOT NULL UNIQUE,
    password_hash   TEXT        NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    date_of_birth   DATE        NOT NULL,
    clearance_level clearance_level NOT NULL DEFAULT 'observer',
    employee_id     VARCHAR(100) NOT NULL UNIQUE,
    is_active       BOOLEAN     NOT NULL DEFAULT TRUE,
    date_joined     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_left       TIMESTAMPTZ,
    session_token   VARCHAR(255) UNIQUE,
    session_token_expires_at TIMESTAMPTZ
);
