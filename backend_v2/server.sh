#!/bin/bash
gunicorn --bind 0.0.0.0:8888 his_doc_setting.asgi:application -k uvicorn.workers.UvicornWorker -w 8 &
nginx

