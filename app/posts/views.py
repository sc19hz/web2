from flask import render_template, redirect, url_for, flash, request, abort,current_app
from flask import Blueprint
from flask_login import current_user, login_required
from app import db
from app.posts.forms import F_post
from app.users.forms import F_Comment
from app.models import Post,User,Comment

posts=Blueprint('posts',__name__)

@posts.route('/post/new',methods=['GET', 'POST'])
def new():
    form=F_post()
    background = url_for('static',filename=f'picture/{current_user.background}')
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully','success')
        return redirect(url_for('main.index'))
    return render_template('new.html',background=background,title='Post a blog',form=form, legend='New Post',tag=2)

@posts.route('/post/<int:postid>', methods=['GET','POST'])
def post(postid):
    post=Post.query.get_or_404(postid)
    user=User.query.get_or_404(post.uid)
    form=F_Comment()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', postid=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    background=url_for('static',filename=f'picture/{user.background}')
    return render_template('post.html',form=form,comments=comments,background=background, title=post.title, post=post,tag=3)

@posts.route('/post/<int:postid>/update', methods=['GET', 'POST'])
@login_required
def update(postid):

    post=Post.query.get_or_404(postid)
    user = User.query.get_or_404(post.uid)
    background=url_for('static',filename=f'picture/{user.background}')
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
    return render_template('new.html',background=background,title='Update',legend='Update Post', form=form,tag=2)

@posts.route('/post/<int:postid>/delete', methods=['POST'])
@login_required
def delete(postid):
    post=Post.query.get_or_404(postid)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('main.index'))