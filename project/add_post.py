from flask import (
        Blueprint, redirect, render_template,
        Response, request, url_for , session
        )
from flask_login import login_user, login_required, logout_user
from project import db
from project.forms import PostForm
from project.models import Post, User


post_bp =  Blueprint('add_post', __name__)

@post_bp.route('/post', methods= ['GET', 'POST'])
@login_required
def adding_posts():
    authorID = session['user_id']
    form = PostForm(request.form)
    if request.method == 'POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            post = Post(authorID, title, text, 0)    
            db.session.add(post)
            db.session.commit()
            user = User.query.filter_by(id=authorID).first()
            return redirect(url_for('feed', user = user))   
        else:
            return Response("<p>invalid form</p>")
    return render_template('add_post.html', form=form)
