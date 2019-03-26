from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/pipeline')
def pipeline():
    return 'pipeline!'


@app.route('/detail')
def detail():
    message = {
        'name':'jack',
        'text':'杰克'
    }
    return render_template('detail.html',info=message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)


