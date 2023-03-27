#!/bin/python3
from app import app
import webview
import threading
from functools import partial

webview.create_window('Gal-BUL Masaüstü Uygulaması', app, width=1191, height=924)
flask_run = partial(app.run, host="0.0.0.0", port=8081, debug=1)

thread_desktop = threading.Thread(target=webview.start)
thread_website = threading.Thread(target=flask_run)

thread_desktop.start()
thread_website.start()