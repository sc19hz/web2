from app.models import Post
from flask import  request, render_template,Blueprint
import logging
main=Blueprint('main',__name__)
from  run import app
@main.route("/")
@main.route("/index")
def index():
    app.logger.info('info log')
    app.logger.warning('warning log')
    pagenumber=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.postdate.desc()).paginate(page=pagenumber, per_page=4)
    return render_template("index.html", posts=posts)

@main.route("/more")
def more():
    return render_template("more.html")