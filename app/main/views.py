from app.models import Post
from flask import  request, render_template,Blueprint,Flask, url_for
from flask_login import current_user,login_required
main=Blueprint('main',__name__)
from  run import app
@main.route("/")
@main.route("/index")
def index():
    background=''
    if current_user.is_authenticated:
        background=url_for('static',filename=f'picture/{current_user.background}')
    app.logger.info('info log')
    app.logger.warning('warning log')
    pagenumber=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.postdate.desc()).paginate(page=pagenumber, per_page=4)
    return render_template("index.html", posts=posts,background=background,tag=1)

@main.route("/more")
def more():
    return render_template("more.html")