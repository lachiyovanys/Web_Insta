from flask import *
from modules.instaloader import Instaloader, Profile, instaloader
from urllib.parse import unquote
import requests
from io import BytesIO
import base64
import asyncio
import aiohttp

auth = Blueprint('auth', __name__)
instance = Instaloader()


def get_code():
    n=1
    code = ""
    try:
        while n<=6:
            code += request.form[f'number{n}']
            n+=1            
        return code
    except Exception as e:
        print("there was an error") 


def abbvr_number(n):
    """Convierte un número a un formato abreviado con 'k', 'M', 'B'."""
    if n < 1000:
        return str(n)
    elif 1000 <= n < 1000000:
        return f"{n/1000:.0f}k"
    elif 1000000 <= n < 1000000000:
        return f"{n/1000000:.0f}M"
    else:
        return f"{n/1000000000:.0f}B"

class Unfollower:
    def __init__(self, username, followers, followees):
        self.username = username
        self.profile_pic_blob = None
        self.isVerified = False
        self.followers = followers
        self.followees = followees
    
    def getisVerified(self):
        return self.isVerified
    
    def setIsVerified(self):
        self.isVerified = True
    
    async def fetch_profile_pic(self):
        try:
            profile = Profile.from_username(instance.context, self.username)
            if profile and profile.profile_pic_url:
                profile_pic_url = unquote(profile.profile_pic_url)
                async with aiohttp.ClientSession() as session:
                    async with session.get(profile_pic_url) as response:
                        if response.status == 200:
                            self.profile_pic_blob = await response.read()
                            return True
                        else:
                            print(f"Error fetching profile pic for {self.username}: HTTP status code {response.status}")
                            return False
            else:
                print(f"Error fetching profile pic for {self.username}: Profile or profile_pic_url is None")
                return False
        except Exception as e:
            print(f"Error fetching profile pic for {self.username}: {str(e)}")
            return False

    def get_profile_pic_data_uri(self):
        if self.profile_pic_blob:
            return f"data:image/jpeg;base64,{base64.b64encode(self.profile_pic_blob).decode('utf-8')}"
        else:
            return None

    def to_dict(self):
        return {
            'username': self.username,
            'followers': self.followers,
            'followees': self.followees,
            'profile_pic_data_uri': self.get_profile_pic_data_uri(),
            'is_Verified': self.getisVerified()
        }

def create_profile(username):
    try:
        profile = Profile.from_username(instance.context, username)
        profile_pic_url = unquote(profile.profile_pic_url) if profile.profile_pic_url else None
        full_name = profile.full_name
        Followers = profile.followers
        Followees = profile.followees
        Posts = 0
        session['full_name'] = full_name
        session['Followees'] = abbvr_number(Followees) 
        session['Followers'] = abbvr_number(Followers)
        session['profile_pic'] = profile_pic_url

        for post in profile.get_posts():
            Posts += 1
        session['Posts'] = abbvr_number(Posts)   
        
        return True
    except Exception as e:
        flash(f"Error creating profile: {str(e)}", category="error")
        return False

async def who_doesnt_follow():
    try:
        profile = Profile.from_username(instance.context, session.get('username'))
        profile_pic_url = unquote(profile.profile_pic_url) if profile.profile_pic_url else None
        session['profile_pic'] = profile_pic_url
        followees = set(profile.get_followees())
        followers = set(profile.get_followers())
        not_following_you = followees - followers

        unfollowers = []
        tasks = []
        
        for user in not_following_you:
            unfollower = Unfollower(user.username, abbvr_number(user.followers), abbvr_number(user.followees))
            if user.is_verified:
                unfollower.setIsVerified()
            tasks.append(asyncio.create_task(unfollower.fetch_profile_pic()))
            unfollowers.append(unfollower)

        await asyncio.gather(*tasks)

        return [unfollower.to_dict() for unfollower in unfollowers]
    except instaloader.ProfileNotExistsException:
        flash("Error")
        return []

@auth.route('/unfollowers', methods=['GET', 'POST'])
def unfollowers():
    if "username" in session:
        username = session.get('username')
        unfollowers = asyncio.run(who_doesnt_follow())
        if unfollowers:
            return render_template('user_profile.html', not_following_you=unfollowers, username=username)
        else:
            flash("No unfollowers found or an error occurred", category="error")
            return render_template('login.html', is_2fa_required=False)
    else:
        flash("You need to log in first", category="error")
        return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_input']
        password = request.form['password_input']
       

        

        try:
            instance.login(username, password)
            session['username'] = username
            if create_profile(username):
                return redirect(url_for('views.main'))
        except instaloader.TwoFactorAuthRequiredException:
            session['is_2fa_required'] = True
            session['username'] = username
            return render_template('code_2FA.html',username = username)
        except instaloader.BadCredentialsException:
            flash("Invalid username or password. Please try again.", category="error")
            return render_template('login.html')
    return render_template('login.html')



@auth.route('/code_2fa',methods=['POST','GET'])
def code_2fa():
    if "username" in session:
        try:
            username = session.get('username')
            print(username)
            two_factor_code = get_code()
            print(two_factor_code)
            instance.two_factor_login(two_factor_code)

            if create_profile(username):
                return redirect(url_for('views.main'))
        except instaloader.BadCredentialsException as e:
                flash("Invalid 2FA code. Please try again.", category="error")
                print(e)
                return redirect(url_for('auth.login'))


    else:
        flash("No 2fa pending.", category="error")
        return redirect(url_for('auth.login'))


@auth.route('/profile-pic')
def profile_pic():
    profile_pic_url = session.get('profile_pic')
    if profile_pic_url:
        try:
            response = requests.get(profile_pic_url)
            if response.status_code == 200:
                return send_file(BytesIO(response.content), mimetype='image/jpeg')
            else:
                return '', 404  # Handle appropriately if profile pic retrieval fails
        except Exception as e:
            print(f"Error fetching profile pic: {str(e)}")
            return '', 404
    return '', 404



@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



@auth.route('/main')
def main():
    if "username" in session:
        username = session.get('username')
        return render_template('main.html', username=username)
    else:
        flash("You need to log in first", category="error")
        return redirect(url_for('auth.login'))
