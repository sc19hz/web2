from app.models import Post,User
from app.users.utils import *
from app.users.forms import F_login,F_registration,F_updateuser
from app import bc,db
from flask import render_template,redirect,flash,Blueprint,request
from flask_login import login_user, current_user,logout_user,login_required

users=Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    form=F_registration()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        npwd=bc.generate_password_hash(form.password.data).decode('uft-8')
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
        db.session.commit()
        flash('User Profile updated successfully','success')
        return redirect(url_for('users.profile'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    picture=url_for('static',filename=f'picture/{current_user.picture}')
    return render_template('profile.html',title='profile',picture=picture,form=form)

@users.route('/user/post/<string:username>', methods=['GET', 'POST'])
def posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    pagenumber=request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.postdate.desc()).paginate(page=pagenumber, per_page=2)
    return render_template('posts.html',user=user,posts=posts,title=f"{username}'s Blog")
