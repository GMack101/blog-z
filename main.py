from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog-z:password@localhost:8889/blog-z'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'ndndfmkhj13@$vds'


class Blog(db.Model): #When this is edited, you need to drop and re-add the Class objects.

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))
   

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model): #When this is edited, you need to drop and re-add the Class objects.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120)) 
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username 
        self.password = password
    def __repr__(self):
        return self.username


@app.route('/')
def index():
    
    user_list=User.query.all()
    return render_template('index.html', user_list=user_list)

@app.route('/login', methods=['GET', 'POST']) 
def login():
    # error variable set to blank

    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            username_error = "User does not exist."

        if username == "":
                username_error = "Please enter your username."

        if password == "":
            password_error = "Please enter your password."

        if user and user.password != password:
            password_error = "That is the wrong password."

        if user and user.password==password:
            session['username'] = user.username
            return redirect('/blog')

        else:
            # change error variable
            flash('wrong username or password', 'error')
        
        #if user != User.query.filter_by(username=username):
                 
                #flash('Logged in') 
                #return redirect('/newpost')

      # if username not in database redirect to login with "user doesnt exist" message 
    #  HTML -  if user doesn't have an account provide link to "create account" and redirect to register page


    # pass error variable into template. 
    # make sure template can handle error variable using jinja2
    return render_template('login.html')




# reimplement code from User-signup to validate registration information
@app.route('/register', methods = ['POST', 'GET']) 
def register():
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        password_error = ""
        username_error = ""
        
        username_db_count = User.query.filter_by(username=username).count() 
        
            

        if username_db_count < 0 or username.strip()=="":
            username_error="That's not a valid username"
            
        

        if password.strip() == "":
            password_error="Invalid Password"
            



        if verify != password: 
            password_error="Invalid Password"
            

                
        if username_error!="" or password_error!="":
            return render_template('signup.html', password_error=password_error, username_error=username_error)
                
        else:
            user = User(username=username,password=password) 
            db.session.add(user)
            db.session.commit() 
            session["username"] = user.username
            return redirect("/")

    return render_template("signup.html")

@app.route("/logout",methods=['POST'])
def logout():

    del session['username']
    return redirect("/blog")

#  def logged_in_user():
#     owner = User.query.filter_by(username=session['username']).first()
#     return owner


@app.before_request
def require_login():
    # Will need to add more allowed routes for not signed in users
    allowed_routes = ['login', 'register', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

 
@app.route('/newpost', methods=['POST', 'GET'])
def add_post():
    title_error=''
    body_error=""

    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]

        if title == "":
            title_error= "Please insert title"
        if body == "":
            body_error= "Please insert body"
        if  title_error!= "" or body_error!="":
            return render_template('new-post.html', title_error=title_error, body_error=body_error)


        else: 
            owner = User.query.filter_by(username=session['username']).first()
            new_post= Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))


       
    return render_template('new-post.html')

#@app.route('/blog', methods=['GET', 'POST']) 
#def main():
    #In this app route we are trying to return a Blog object.






@app.route('/blog', methods=['GET'])
def blog():
    user= request.args.get("username")
    username = User.query.filter_by(username=user).first()
    if username:
        bloglist = Blog.query.filter_by(owner=username).all()
        
        return render_template('blog.html',bloglist=bloglist)
    else:
        bloglist=Blog.query.all()
        blog_id=request.args.get('id') 
        blog_post= Blog.query.get(blog_id)
        return render_template('blog.html', blog_post=blog_post, bloglist=bloglist)
    
    bloglist = Blog.query.all()
    return render_template('blog.html',bloglist=bloglist)

        
if __name__ == '__main__':
    app.run()


#@app.route('/blog')
#def blog():
 #   if request.args.get('username')
  #  user_id=User.query.filter_by(username=username).first().id
   # blog_id=request.args.get('id')
    # blog_post= Blog.query.get(blog_id)
   # blog_list= Blog.query.all()

# need if statement to be able to use a return statement
    #blog_list = Blog.query.filter_by(owner=owner).all()  
   # return render_template('blog.html',title="Blog-z!", blog_list=blog_list)  
#return render_template("blog.html", blog_list=blog_list, blog_post=blog_post)

# be able to see a complete list of registered users via the "/" (even if not logged in)
# select all the blogs from a single user and display with the single user.html
# Add author tag to blogs on main list and individual posts using owner_id




    