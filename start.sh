#!/bin/bash
gunicorn --bind unix:app:sock src:app -m 007