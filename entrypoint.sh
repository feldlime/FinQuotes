#!/usr/bin/env bash

gunicorn project:create_app -c gunicorn.conf.py

