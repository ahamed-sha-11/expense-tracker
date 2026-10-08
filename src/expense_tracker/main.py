import uvicorn


def main():
    uvicorn.run("expense_tracker.app:app", reload=True, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
