from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kebabop babob'

from app import routes

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)