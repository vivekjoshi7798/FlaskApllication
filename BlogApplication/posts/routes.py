from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from BlogApplication.posts.forms import postForm
from BlogApplication.models import Post
from BlogApplication import db
from flask_login import current_user, login_required

posts = Blueprint('posts', '__name__')


@posts.route("/Post/Create_post", methods=['POST', 'GET'])
@login_required
def Create_post():
    form = postForm()
    if form.validate_on_submit():
        post = Post(title=form.Title.data, content=form.Content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('POSTED SUCESSFULLY', 'SUCESS')
        return redirect(url_for('mains.home'))
    return render_template('Create_Post.html', title='Update_a_post', legend='Say in Your Words', form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post, title='post')


@posts.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
def UpdatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = postForm()
    if form.validate_on_submit():
        post.title = form.Title.data
        post.content = form.Content.data
        db.session.commit()
        flash("post Updated", 'Sucess')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.Title.data = post.title
        form.Content.data = post.content
    return render_template('Create_Post.html', title='Update_a_post', legend='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('mains.home'))
