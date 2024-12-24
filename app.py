from flask import Flask, render_template
from config import Config

app = Flask(__name__,
    template_folder='app/templates',
    static_folder='app/static'
)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes/index.html', clientes=[])

if __name__ == '__main__':
    app.run(debug=True) 