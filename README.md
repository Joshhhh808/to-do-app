# Tasks — A Simple To-Do List Web App

A minimal to-do list app built with Flask and SQLite. Add tasks, mark them
done, delete them. No frameworks on the frontend beyond plain HTML/CSS —
the whole thing is intentionally small so it's easy to read end to end.

## Features

- Add a task
- Mark a task complete / incomplete
- Delete a task
- Data persists in a SQLite database file (survives container restarts
  when you mount a volume — see below)

## Tech stack

- **Backend:** Python, Flask
- **Storage:** SQLite (via Python's built-in `sqlite3`)
- **Frontend:** HTML + CSS (Jinja2 templates, no JS framework)
- **Containerization:** Docker

## Project structure
