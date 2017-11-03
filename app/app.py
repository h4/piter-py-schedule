from flask import Flask, Response

from .generate_calendar import generate

app = Flask(__name__)


@app.route('/')
def main():
    calendar = generate()
    resp = Response(calendar.decode(), mimetype='text/calendar')
    resp.headers["content-disposition"] = 'attachment; filename="piter-py.ics"'
    return resp


if __name__ == '__main__':
    app.run()

