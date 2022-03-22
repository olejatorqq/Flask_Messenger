from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Text %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-chat', methods=['POST', 'GET'])
def sendMessage():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        text = Text(name=name, message=message)

        try:
            db.session.add(text)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении сообщения произошла ошибка"
    else:
        return render_template("create-chat.html")




if __name__ == "__main__":
    app.run(debug=True)