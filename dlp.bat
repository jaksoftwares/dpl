@echo off
cd /d C:\Users\josep\dpl
call venv\Scripts\activate
start "" http://127.0.0.1:8000
waitress-serve --listen=127.0.0.1:8000 dpl_core.wsgi:application