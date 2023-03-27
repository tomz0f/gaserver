#!/bin/python3
from app import app
import webview
import os

path = os.getcwd()
os.environ["OPENSSL_CONF"] = path+'/openssl.cnf'

webview.create_window('Gal-BUL Masaüstü Uygulaması', app, width=1191, height=924)
webview.start()
