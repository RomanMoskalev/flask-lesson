from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/posts")
def posts():
    posts = Post.query.order_by(Post.id.desc()).all()

    return render_template("posts.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]

        post = Post(title=title, text=text)

        db.session.add(post)
        db.session.commit()

    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)