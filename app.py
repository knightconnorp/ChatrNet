from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os, datetime, string, random, secrets
from sqlalchemy import desc, Boolean
from werkzeug.utils import secure_filename

# Using dictionary to store both the short value and the long value for a place together
place_list = {'r':'Random *NSFW*', 't':'Tech', 'm':'Memes', 'n':'World News'}
admin_key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
print("Admin Key: " + admin_key)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = secrets.token_hex()
db = SQLAlchemy(app)

class Post(db.Model):
    _id = db.Column("name", db.Integer, primary_key=True)
    title = db.Column("title", db.String(24), nullable=False)
    username = db.Column("username", db.String(24), nullable=False)
    date = db.Column("date", db.String(100), nullable=False)
    content = db.Column("content", db.String(256), nullable=False)
    filepath = db.Column("filepath", db.String(256), nullable=False)
    place = db.Column("place", db.String(4), nullable=False)
    adminkey = db.Column("adminkey", Boolean, nullable=False)
    def __init__(self, title, username, content, filepath, place, adminkey):
        self.title = title
        self.username = username
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f").rstrip('0')
        self.content = content
        self.filepath = filepath
        self.place = place
        self.adminkey = adminkey

    @property
    def id(self):
        return self._id


# create db table if not exist
with app.app_context():
    db.create_all()

# if uploads does not exist, create it
if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home', posts=Post.query.order_by(desc(Post._id)).limit(4).all(), place_list=place_list)

@app.route('/post', methods=['GET', 'POST'])
def post_page():
    if request.method == 'GET':
        return render_template('post.html', title='Post', place_list=place_list)
    elif request.method == 'POST':
        title=request.form['title']
        username=request.form['username']
        content=request.form['content']
        file = request.files['file']
        place = request.form['place']
        adminkey_input = request.form['adminkey']
        adminkey_bool=False
        if username == '':
            username = "Anonymous"
        if admin_key == adminkey_input:
            adminkey_bool = True
        if file.filename == '':
            filepath = "None"
            new_post = Post(title, username, content, filepath, place, adminkey_bool)
            db.session.add(new_post)
            db.session.commit()
        else:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_post = Post(title, username, content, filepath, place, adminkey_bool)
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/<place>')
def places(place):
    if place in place_list:
        return render_template('place.html', title=place_list[place], place=place, posts=Post.query.order_by(desc(Post._id)).filter(Post.place==place).all(), place_list=place_list)
    else:
        return render_template('error.html', title='Error')

@app.route('/terms')
def terms():
    return render_template('terms.html', title='Terms')

if __name__ == '__main__':
    app.run(debug=True)
