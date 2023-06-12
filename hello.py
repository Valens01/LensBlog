from unicodedata import name
from wsgiref import validate
from flask import Flask, flash, render_template ,flash,request,redirect,url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from webform import LoginForm,PostForm, UsersForm,PasswordForm,NamerForm,SearchForm
from flask_ckeditor import CKEditor




#------------------------------------##########################################-------------------------------------
#create a flask instense

app = Flask(__name__)

#initialize ckeditor
ckeditor = CKEditor(app)
#add Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
#secret keyy----
app.config['SECRET_KEY']= "... THE SECRET KEY... "
#iinitilize the database
db=SQLAlchemy(app)
migrate=Migrate(app,db)


#setup login flask
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))

#pass stuff to the nav
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)



#--------------------------################################################---------------------------------

#create a model
class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    name= db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    favorite_color=db.Column(db.String(100))
    password_hash= db.Column(db.String(128))
    date_added=db.Column(db.DateTime,default=datetime.utcnow)
    posts=db.relationship('Post',backref='poster')
   

    @property
    def password(self):
        raise AttributeError("its not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash= generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self) :
        return '<Name %r>' % self.name



#create Lens blog model
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.Text)
   # author=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime,default=datetime.utcnow)
    slug=db.Column(db.String(255))
    poster_id=db.Column(db.Integer(),db.ForeignKey('users.id'))





#-----------------##############################################----------------------------------------------


#create a route decorator

#admin pge
@app.route('/admin')
def admin():
   id= current_user.id
   if id == 5:
     return render_template("admin.html")
   else:
     flash("you can't access to this page")
     return redirect('url_for("dashboard")')



#search
@app.route("/search", methods=['POST'])
def search():
    form=SearchForm()
    posts=Post.query
    if form.validate_on_submit():
        post.searched= form.searched.data 

        posts= posts.filter(Post.content.like('%'+post.searched +'%'))
        posts= posts.order_by(Post.title).all()
    return render_template("search.html",form=form,searched=post.searched,posts=posts)

   


#create a login page
@app.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user =Users.query.filter_by(username=form.username.data).first()
        if user:
            #check hash password
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("login successfully")
                return redirect(url_for("dashboard"))
            else:
                flash("wrong password, Try again....")
        else:
             flash("wrong username, Try again....")

    return render_template("login.html",form=form)

    #create the logout for the user

@app.route("/logout",methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("login"))




#create a Dashbord
@app.route("/dashboard",methods=["POST","GET"])
@login_required
def dashboard():
    id = current_user.id
    form=UsersForm()
    name_to_update= Users.query.get_or_404(id) 
    if request.method=='POST':
        name_to_update.name= request.form['name']
        name_to_update.email= request.form['email']
        name_to_update.favorite_color= request.form['favorite_color']
        name_to_update.username= request.form['username']
        try:
            db.session.commit()
            flash("user as been updated")
            return(render_template("dashboard.html",
            form=form,
            name_to_update=name_to_update,id=id))
        except:
             flash("error! look like they was a problem, try again")
             return(render_template("update.html",
             form=form,
             name_to_update=name_to_update))
    else:
        return(render_template("dashboard.html",
             form=form,
             name_to_update=name_to_update,id=id))
    #return render_template("dashboard.html")



#all the post page on the blog
@app.route("/posts")
def posts():
    #grab from the databse all the post
    posts=Post.query.order_by(Post.date_posted)
    return render_template("posts.html",posts=posts)



#individuell blog post
@app.route("/posts/<int:id>")
def post(id):
    post=Post.query.get_or_404(id)
    return render_template("post.html",post=post)




#edit the blos post

@app.route("/posts/edit/<int:id>",methods=["POST","GET"])
@login_required
def edit_posts(id):
    form=PostForm()
    post=Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title=form.title.data
        post.slug=form.slug.data
        post.content=form.content.data
         #add the post to the database
        db.session.add(post)
        db.session.commit()
        flash("Post has been edited")
        return redirect(url_for("post",id=post.id))
    if current_user.id== post.poster_id:
        form.title.data=post.title
        form.content.data=post.content
        form.slug.data=post.slug
        return render_template("edit_post.html",form=form)
    else:
        flash("you can't delete this post")
        post=Post.query.get_or_404(id)
        return render_template("post.html",post=post)



#delete post
@app.route("/post/delete/<int:id>",methods=["POST","GET"])
@login_required
def delete_post(id):
    post_to_delete=Post.query.get_or_404(id)
    ad = current_user.id
    if ad == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("blog post has been deleted")

            posts=Post.query.order_by(Post.date_posted)
            return render_template("posts.html",posts=posts)
        except:
            flash("there was a problem")
            posts=Post.query.order_by(Post.date_posted)
            return render_template("posts.html",posts=posts)
    else:
        flash("You can't delete this post")

        posts=Post.query.order_by(Post.date_posted)
        return render_template("posts.html",posts=posts)




#add post page
@app.route("/addPost",methods=['POST','GET'])
@login_required
def add_post():

    form = PostForm()
    if form.validate_on_submit():
        poster= current_user.id
        post=Post(title=form.title.data,poster_id=poster,content=form.content.data,slug=form.slug.data)
        #just claer the form
        form.title.data=""
        form.content.data=""
        form.slug.data=""

        #add the post to the database
        db.session.add(post)
        db.session.commit()
        flash("The post is Added successfully")
    return render_template("add_post.html",form=form)


#return json
@app.route("/date")
def current_date():
    return {'Date':date.today()} 

#delete user
@app.route("/delete/<int:id>", methods=['POST','GET'])
def delete(id):
   
    user_to_delete=Users.query.get_or_404(id)
    name=None
    form=UsersForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("an user as been deleted")
        our_users=Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
        form=form,
        name=name,
         our_users=our_users)
    except:
        flash("there is a problem..... try again")
        



#update record
@app.route('/update/<int:id>', methods=['POST','GET'])
@login_required
def update(id):
    form=UsersForm()
    name_to_update= Users.query.get_or_404(id) 
    if request.method=='POST':
        name_to_update.name= request.form['name']
        name_to_update.email= request.form['email']
        name_to_update.favorite_color= request.form['favorite_color']
        name_to_update.username= request.form['username']
        try:
            db.session.commit()
            flash("user as been updated")
            return(render_template("update.html",
            form=form,
            name_to_update=name_to_update,id=id))
        except:
             flash("error! look like they was a problem, try again")
             return(render_template("update.html",
             form=form,
             name_to_update=name_to_update))
    else:
        return(render_template("update.html",
             form=form,
             name_to_update=name_to_update,id=id))



#add user to the database

@app.route('/user/add',methods=['POST','GET'])
def add_user():
    name=None
    form=UsersForm()
    if form.validate_on_submit():
        user= Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash the  password 
            hashed_password= generate_password_hash(form.password_hash.data,"sha256")
            user=Users(name=form.name.data,username=form.username.data,email= form.email.data,favorite_color=form.favorite_color.data,password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=""
        form.username.data=""
        form.email.data=""
        form.favorite_color.data=""
        form.password_hash.data=""
        flash("user added successfully") 
    our_users=Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
    form=form,
    name=name,
    our_users=our_users)


#create a test for password
@app.route('/test_pw',methods=['GET','POST'])

def test_pw():
    email=None
    password=None
    pw_to_check=None
    passed=None
    form= PasswordForm()
    #validate the form
    if form.validate_on_submit():
        email= form.email.data
        password=form.password.data
        form.email.data=''
        form.password.data=''
        #lookup  to find the email
        pw_to_check= Users.query.filter_by(email=email).first()

        #checkout if the password is valid or not
        passed = check_password_hash(pw_to_check.password_hash,password)

    return render_template("test_pw.html",email=email,password=password,passed=passed, pw_to_check= pw_to_check ,form=form)



@app.route('/')
def index():
    fisrt_name="valens"
    favarite_pizza=["peperoni","cheesse",42]
    return render_template("index.html",fisrt_name=fisrt_name, favarite_pizza= favarite_pizza)

#localhost :5000/user/vava
@app.route('/user/<name>')

def user(name):
    return render_template("user.html",user_name=name)


@app.route('/name',methods=['GET','POST'])

def name():
    name=None
    form= NamerForm()
    #validate the form
    if form.validate_on_submit():
        name= form.name.data
        form.name.data=''
        flash("form submitted successfully")
    return render_template("name.html",name=name, form=form)


#create custom error page
#invalid url
@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"), 404


#internal server not found
@app.errorhandler(500)

def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)







