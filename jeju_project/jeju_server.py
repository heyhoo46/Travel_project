from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('jeju.html')

@app.route('/market.html')
def market():
    return render_template('market.html')

@app.route('/orem.html')
def orem():
    return render_template('orem.html')

@app.route('/dullegil.html')
def dullegil():
    return render_template('dullegil.html')

@app.route('/museum.html')
def museum():
    return render_template('museum.html')

@app.route('/entertain.html')
def entertain():
    return render_template('entertain.html')

@app.route('/mountain.html')
def mountain():
    return render_template('mountain.html')

@app.route('/beach.html')
def beach():
    return render_template('beach.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
