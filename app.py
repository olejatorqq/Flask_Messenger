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


@app.route('/posts')
def getChat():
    messages = Text.query.order_by(Text.id.desc()).all()
    return render_template("posts.html", messages=messages)


@app.route('/create-chat', methods=['POST', 'GET'])
def sendMessage():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        text = Text(name=name, message=message)

        try:
            db.session.add(text)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении сообщения произошла ошибка"
    else:
        return render_template("create-chat.html")


@app.route('/posts/<int:id>/delete')
def delChat(id):
    chat = Text.query.get_or_404(id)

    try:
        db.session.delete(chat)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении сообщения произошла ошибка"



@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def updateMessage(id):
    chat = Text().query.get(id)
    if request.method == 'POST':
        chat.name = request.form['name']
        chat.message = request.form['message']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При изменении сообщения произошла ошибка"
    else:
        return render_template("post_update.html", chat=chat)


if __name__ == "__main__":
    app.run(debug=True)
