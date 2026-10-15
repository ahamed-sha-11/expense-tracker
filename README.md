# Expense Tracker API

A small API I'm building to learn FastAPI. You sign up, log in, and keep track of your own expenses and categories. Nobody else can see your data.

Built with FastAPI, async SQLAlchemy (SQLite), Redis for login sessions, and uv.

## Run it

You need Python 3.14, [uv](https://docs.astral.sh/uv/), and Redis running locally.

```bash
uv sync
uv run uvicorn expense_tracker.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

## Try it

1. Sign up with `POST /users/`.
2. Click **Authorize** and log in with your email and password.
3. Add some categories and transactions.

There's a shared **Miscellaneous** category (id `-1`) everyone can use.

## Good to know

- There are no migrations yet. If you change a model, delete `test.db` and restart.
- `DATABASE_URL` and `REDIS_URL` can be set as environment variables.
