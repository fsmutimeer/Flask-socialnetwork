from flask import render_template, url_for, redirect,flash,request,Blueprint,abort
from flask_login import current_user, login_required
from project import db
from project.models import BlogPost
from project.blog_posts.forms import BlogPostForm

blog_posts_blueprint = Blueprint('blog_posts',__name__)

#CRUD
#Create
@blog_posts_blueprint.route('/create',methods=['GET','POST'])
@login_required
def create():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post= BlogPost(title=form.title.data,text=form.text.data,user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post Created')
        return redirect(url_for('core.index'))
    return render_template('create-post.html',form=form)
#View blogpost
@blog_posts_blueprint.route('/<int:blog_post_id>')
def view_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog-post-view.html',title=blog_post.title,date=blog_post.date,post=blog_post)
#update
@blog_posts_blueprint.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title=form.title.data
        blog_post.text=form.text.data
       
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog-post-view',blog_post_id=blog_post.id))

    elif request.method =='GET':
        form.title.data=blog_post.title
        form.text.data = blog_post.text
    return render_template('create-post.html',title='Updating',form=form)


#delete
@blog_posts_blueprint.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    return redirect('core.index')