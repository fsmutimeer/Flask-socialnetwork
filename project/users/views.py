# Project/users/views.py

from flask import render_template, url_for, redirect, Blueprint,flash,request
from project import db
from flask_login import login_user,logout_user, current_user, login_required
from project.models import User, BlogPost
from project.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from project.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)
#Register
@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user =User( email = form.email.data,
                        username = form.username.data,
                        password = form.password.data,
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('Thank for registering')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)
#login
@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user= User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:


            login_user(user)

            flash('You are logged in')

            next = request.args.get('next')
            if next ==None or not next[0]=='/':
                next=url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


#logout
@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('core.index'))
#account(UpdateUserForm)

@login_required
@users.route('/account',methods=['POST','GET'])

def account():
    form=UpdateUserForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image=pic
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile Updated successfully')
        return redirect(url_for('users.account'))
        
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data=current_user.email

    profile_image = url_for('static',filename='profile_pic/'+current_user.profile_image)

    return render_template('account.html',form=form,profile_image=profile_image)
#user's list of blog posts
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user= User.query.filter_by(username=username).first_or_404()
    blog_posts = User.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',user=user,blog_posts=blog_posts )



