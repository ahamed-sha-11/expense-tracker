# Expense Tracker API

A simple API for tracking your expenses, built while learning FastAPI.

## What it does

- Sign up and log in
- Create your own categories (Food, Rent, ...)
- Add, edit and delete transactions
- Your data is private: other users can't see it

If you add a transaction without a category, it goes into **Miscellaneous**.

## Getting started

The app uses **PostgreSQL** and **Redis**. The easiest way to run everything is **Docker Compose**.

1. Copy `.env.example` to `.env` and fill in the values.
2. Start the database, Redis and the app:

```bash
docker compose up --build
```

Open **http://127.0.0.1:8080/docs** in your browser.

Inside Docker Compose the app reaches PostgreSQL at the hostname `db` and Redis at `redis`.

### Running the app outside Docker

You'll need **Python 3.14** and **[uv](https://docs.astral.sh/uv/)**. Start only PostgreSQL and Redis with Compose,
then point the app at `localhost` instead of `db`:

```bash
docker compose up -d db redis
uv sync
DATABASE_URL=postgresql+asyncpg://expense_user:<password>@localhost:5432/expense_tracker \
  uv run uvicorn expense_tracker.main:app --reload
```

Open **http://127.0.0.1:8000/docs** in your browser.

## How to use it

1. Create an account with `POST /users/`
2. Click **Authorize** at the top of the page and log in with your **email** and password
3. You can now use the category and transaction endpoints

## Endpoints

All category and transaction endpoints need you to be logged in.

**Users**

| Method | Endpoint         | What it does                 |
|--------|------------------|------------------------------|
| POST   | `/users/`        | Create an account            |
| POST   | `/users/login`   | Log in                       |
| POST   | `/users/logout`  | Log out                      |
| GET    | `/users/me`      | See your account             |

**Categories**

| Method | Endpoint            | What it does                                  |
|--------|---------------------|-----------------------------------------------|
| GET    | `/categories/`      | List your categories (plus Miscellaneous)     |
| POST   | `/categories/`      | Create a category                             |
| GET    | `/categories/{id}`  | Get one category                              |
| PATCH  | `/categories/{id}`  | Rename a category                             |
| DELETE | `/categories/{id}`  | Delete a category (only if it has no transactions) |

Miscellaneous is shared by everyone, so it can't be renamed or deleted.

**Transactions**

| Method | Endpoint              | What it does              |
|--------|-----------------------|---------------------------|
| GET    | `/transactions/`      | List your transactions    |
| POST   | `/transactions/`      | Add a transaction         |
| GET    | `/transactions/{id}`  | Get one transaction       |
| PATCH  | `/transactions/{id}`  | Edit a transaction        |
| DELETE | `/transactions/{id}`  | Delete a transaction      |

Lists are paged: add `?page=2&size=20` to the URL.

## Built with

FastAPI · SQLAlchemy · PostgreSQL · Redis · uv

## Note

There are no database migrations yet. Tables are created on startup, but existing tables are never changed.
If you change a model, drop the affected table in PostgreSQL (or reset the database) and restart the app.
