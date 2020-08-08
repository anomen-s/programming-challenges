from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index.html')
def index():
    return '<h1>title</h1>', 201

@app.route('/mesta')
def mesta():
    return render_template("mesta.csv")

@app.errorhandler(404)
def e404(e):
    return '<h1>not found</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)
