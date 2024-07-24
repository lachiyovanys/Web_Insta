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

@views.route('/main')
def main():
    if "username" in session:
        username = session.get('username')
        profile_pic_url = session.get('profile_pic')
        full_name = session.get('full_name')
        Followees = session.get('Followees')
        Followers = session.get('Followers')
        Posts = session.get('Posts')
        return render_template('main.html', username=username,full_name = full_name, Followers = Followers, Followees = Followees, profile_pic_url = profile_pic_url, Posts = Posts)
    
    else:
        return redirect(url_for('auth.login'))    