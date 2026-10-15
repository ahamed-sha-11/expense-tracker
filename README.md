# Expense Tracker API

A simple API for tracking your expenses, built while learning FastAPI.

## What it does

- Sign up and log in
- Create your own categories (Food, Rent, ...)
- Add, edit and delete transactions
- Your data is private: other users can't see it

If you add a transaction without a category, it goes into **Miscellaneous**.

## Getting started

You'll need **Python 3.14**, **[uv](https://docs.astral.sh/uv/)** and **Redis** running on your machine.

```bash
uv sync
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

FastAPI · SQLAlchemy · SQLite · Redis · uv

## Note

There are no database migrations yet. If you change a model, delete `test.db` and restart the app.
