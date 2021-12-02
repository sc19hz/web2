from flask import render_template, redirect, url_for, flash, request, abort
from flask import Blueprint
from flask_login import current_user, login_required
from app import db
from app.posts.forms import F_post
from app.models import Post

posts=Blueprint('posts',__name__)

@posts.route('/post/new',methods=['GET', 'POST'])
def new():
    form=F_post()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully','success')
        return redirect(url_for('main.index'))
    return render_template('new.html',title='Post a blog',form=form, legend='New Post')

@posts.route('/post/<int:postid>', methods=['GET'])
def post(postid):
    post=Post.query.get_or_404(postid)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:postid>/update', methods=['GET', 'POST'])
@login_required
def update(postid):
    post=Post.query.get_or_404(postid)
    form=F_post()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The post is updated','success')
        return redirect(url_for('posts.post',postid=postid))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new.html',title='Update',legend='Update Post', form=form)

@posts.route('/post/<int:postid>/delete', methods=['POST'])
@login_required
def delete(postid):
    post=Post.query.get_or_404(postid)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('main.index'))