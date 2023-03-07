from flask import Flask
import time

time.sleep(40)

app = Flask(__name__)

from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.debug = True

from app import views
