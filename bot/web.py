"""Bot Web Server."""

from threading import Thread

from flask import Flask

app = Flask(__name__)

@app.route("/status")
def status():
    """Health Check."""
    return "OK"


def run():
    """Run the Flask App."""
    app.run(host="0.0.0.0", port=5000)


def keep_alive():
    """Server Thread."""
    server = Thread(target=run)
    server.start()
