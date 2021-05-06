from flask import render_template, url_for, flash, redirect, request
from BlogApplication.users.forms import registrationForm, LoginForm, UpdateForm,  RequestResetForm, ResetPasswordForm
from BlogApplication.models import User, Post
from BlogApplication import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from BlogApplication.users.Utils import save_Picture,sendMail


from flask import Blueprint

users= Blueprint('users','__name__')


@users.route("/Login", methods=['POST', 'GET'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('mains.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.Password.data):
            login_user(user, remember=form.Remember.data)
            flash('Successful LOGIN', 'SUCCESS')
            text_page = request.args.get('next')
            if text_page:
                return redirect(text_page) if text_page else redirect(url_for('mains.home'))
            return redirect(url_for('mains.home'))
        else:
            flash('Login Failed ', 'FAILED')
            print('Incorrect Values')
    return render_template('Login.html', title='Login', form=form)


@users.route("/Register", methods=['POST', 'GET'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('mains.home'))
    form = registrationForm()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.Password.data)
        user_1 = User(username=form.Username.data, password=pass_hash, email=form.Email.data)
        db.session.add(user_1)
        db.session.commit()
        flash('Successful Login', 'SUCCESS')
        return redirect(url_for('users.Login'))
    else:
        flash('Failed LOGIN', 'DANGER')
    return render_template('Register.html', title='REG', form=form)





@users.route("/Logout", )
def Logout():
    logout_user()
    return redirect(url_for('users.Login'))


@users.route("/Account", methods=['POST', 'GET'])
@login_required
def Account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            data1 = save_Picture(form.picture.data)
            current_user.image_file = data1
        current_user.username = form.Username.data
        current_user.email = form.Email.data
        db.session.commit()
        flash('ACCOUNT UPDATED ', 'SUCCESS')
        return redirect(url_for('users.Account'))
    elif request.method == 'GET':
        form.Username.data = current_user.username
        form.Email.data = current_user.email
    imagefile = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('Account.html', title='Account', imagefile=imagefile, form=form)

@users.route("/User/<string:username>")
def UserPost(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, title='Home', user=user)

@users.route("/reset_password/", methods=['POST', 'GET'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('mains.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        print(user)
        sendMail(user)
        flash('Verification Link has been sent to your Email', 'success')
        return redirect(url_for('users.Login'))
    return render_template('reset_request.html', title='Reset Password', form=form)




@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('mains.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.Login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
