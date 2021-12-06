import hashlib
from flask import make_response

import app
from app.models import Post,User,Follow
from app.users.utils import *
from app.users.forms import F_login,F_registration,F_updateuser,F_reset,F_quest
from app import bc,db
from flask import abort, render_template,redirect,flash,Blueprint,request
from flask_login import login_user, current_user,logout_user,login_required
from functools import wraps



users=Blueprint('users',__name__)

@staticmethod
def geneAuthCode(user=None):

    m=hashlib.md5()
    str="%s-%s-%s-%s-%s"%(user.id,user.username,user.email,user.picture,user.password)
    m.update(str.encode("utf-8"))
    response = make_response()
    response.set_cookie(app.Config['AUTH_COOKIE_NAME'],"%s#s"%(m.hexdigest(),user.id))
    return response


@users.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('users.posts', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('users.posts', username=username))

@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    print(1)
    if current_user.is_following(user):
        current_user.unfollow(user)
        flash('You are now not following %s.' % username)
    return redirect(url_for('users.posts', username=username))


@users.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    background=url_for('static',filename=f'picture/{user.background}')
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page,
        error_out=False)
    pagination1=user.followed.paginate(
        page,
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
                for item in pagination.items]
    followeds=[{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination1.items]
    if not followeds:
        print(1)
    return render_template('followers.html',background=background, user=user, title="Followers of",
                            endpoint='.followers', pagination=pagination,pagination1=pagination1,
                            follows=follows,followeds=followeds,tag=1)



@users.route("/register",methods=['GET','POST'])
def register():
    form=F_registration()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        npwd=bc.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=npwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account registration success','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)

@users.route("/login",methods=['GET','POST'])
def login():

    form=F_login()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bc.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next=request.args.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(url_for('main.index'))
        else:
            flash(f"Wrong email or password",'danger')
    return render_template('login.html',title='Login',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form=F_updateuser()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            picturename=edit_picture(current_user.username, form.picture.data)
            current_user.picture=picturename
        if form.background.data:
            backgroundname = edit_background(current_user.username, form.background.data)
            current_user.background = backgroundname
        db.session.commit()
        flash('User Profile updated successfully','success')
        return redirect(url_for('users.profile'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    picture=url_for('static',filename=f'picture/{current_user.picture}')
    background=url_for('static',filename=f'picture/{current_user.background}')
    return render_template('profile.html',title='profile',picture=picture,background=background,form=form,tag=2)

@users.route('/user/post/<string:username>', methods=['GET', 'POST'])
def posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    background=url_for('static',filename=f'picture/{user.background}')
    pagenumber=request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.postdate.desc()).paginate(page=pagenumber, per_page=4)
    return render_template('posts.html',background=background,user=user,posts=posts,title=f"{username}'s Blog",tag=1)

@users.route('/resetpwd',methods=['GET','POST'])
def req_reset():
    form=F_quest()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        reset_email(user)
        flash('An email has been sent with further instructions', 'info')
        return redirect(url_for('users.login'))
    return render_template('questreset.html', title='Reset Password',form=form)

@users.route('/resetpwd/<token>',methods=['GET', 'POST'])
def reset_token(token):
    form=F_reset()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for(users.reqreq_reset))
    if form.validate_on_submit():
        npwd = bc.generate_password_hash(form.password.data).decode('utf-8')
        user.password = npwd
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset.html', title='Reset Password', form=form)

@users.route('/pwdreset',methods=['GET','POST'])
@login_required
def pwdreset():
    form=F_reset()
    if form.validate_on_submit():
        npwd = bc.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = npwd
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('reset.html', title='Reset Password', form=form)