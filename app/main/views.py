from app.models import Post
from flask import  request, render_template,Blueprint

main=Blueprint('main',__name__)

@main.route("/")
@main.route("/index")
def index():
    pagenumber=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.postdate.desc()).paginate(page=pagenumber, per_page=4)
    return render_template("index.html", posts=posts)

@main.route("/more")
def more():
    return render_template("more.html")