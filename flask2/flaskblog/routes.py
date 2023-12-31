from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
posts = [
    {
        'author': 'blog post 1',
        'title': 'my 1st web',
        'content': 'practice',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'blog post',
        'title': 'my 1st web',
        'content': 'practice',
        'date_posted': 'April 20, 2018'
    }
]
#name of module flask app


#route what we type to the browser to get to the web we want
#route decorator give additional functionality to the existing function
#/ root page of our web
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
             return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'your account has been created!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page(next_page) else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful, Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)
@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
     return render_template('account.html', title='Account', image_file=image_file)
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
     form = PostForm()
     if form.validate_on_submit():
          flash('Your post has been created', 'success')
          return redirect(url_for('home'))
     return render_template('create_post.html', title='New Post', form=form)
     