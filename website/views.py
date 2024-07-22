from flask import Blueprint, render_template, session, redirect, url_for
import time


views = Blueprint('views', __name__)

@views.route('/')
def splash_page():
    session.clear()
    return render_template('splash_page.html')



@views.route('/user_profile')
def user_profile():
    if "username" in session:
        username = session.get('username')
        profile_pic_url = session.get('profile_pic')

        
        return render_template('user_profile.html', username=username, profile_pic_url=profile_pic_url)
    else:
        return redirect(url_for('auth.login'))
    