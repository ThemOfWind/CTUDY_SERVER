#!/bin/bash
gunicorn --bind 0.0.0.0:8888 settings.asgi:application -k uvicorn.workers.UvicornWorker -w 8 &
nginx

