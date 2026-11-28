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

`GET /transactions/` returns the page together with paging details:

```json
{
  "items": [ ... ],
  "total": 556,
  "page": 2,
  "size": 20,
  "total_pages": 28,
  "has_next": true,
  "has_previous": true
}
```

`total` counts every transaction that matches your filters, not only the ones on this page.
Asking for a page past the end returns an empty `items` list.

**Filtering transactions**

`GET /transactions/` accepts these optional filters. Use any of them together; a transaction must match all of them.

| Filter             | Example                              | Meaning                                  |
|--------------------|--------------------------------------|------------------------------------------|
| `transaction_type` | `1` or `2`                           | `1` = income, `2` = expense              |
| `category`         | `5`, `-1`                            | Only this category id                    |
| `start_date`       | `2026-10-01T00:00:00%2B05:30`        | On or after this time (needs a time zone)|
| `end_date`         | `2026-10-31T23:59:59Z`               | On or before this time (needs a time zone)|

Example: expenses in category 5 during October 2026 (India time):

```
/transactions/?transaction_type=2&category=5&start_date=2026-10-01T00:00:00%2B05:30&end_date=2026-10-31T23:59:59%2B05:30
```

In a URL, write `+05:30` as `%2B05:30` (a plain `+` is read as a space), or use `Z` for UTC.
`start_date` after `end_date` returns 422.

## Built with

FastAPI · SQLAlchemy · PostgreSQL · Redis · uv

## Note

There are no database migrations yet. Tables are created on startup, but existing tables are never changed.
If you change a model, drop the affected table in PostgreSQL (or reset the database) and restart the app.
