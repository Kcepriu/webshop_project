
from flask import Flask, abort


app = Flask(__name__)
@app.route('/')
def index():
    return 'helo word'

app.run(debug=True)