from app import app
import webview

webview.create_window('Gal-BUL Masaüstü Uygulaması', app, width=1191, height=924)
webview.start()