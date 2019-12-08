from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body


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

            new_post= Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))


       
    return render_template('new-post.html')

@app.route('/blog')
def blog():
    blog_id=request.args.get('id')
    blog_post= Blog.query.get(blog_id)
    blog_list= Blog.query.all()
    
    
    
    
    return render_template("blog.html", blog_list=blog_list, blog_post=blog_post)





if __name__ == '__main__':
    app.run()