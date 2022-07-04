try:
    from flask import Flask,render_template,url_for,request,redirect, make_response
    import json
    from flask import Flask, render_template, make_response
    from flask_dance.contrib.github import make_github_blueprint, github
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 
    from dotenv import load_dotenv
    load_dotenv()

    GITHUB_CLIENT_ID = os.getenv('CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
except Exception as e:
    print("Some Modules are Missings {}".format(e))
    

app = Flask(__name__)
app.config["SECRET_KEY"]="SECRET KEY  "

github_blueprint = make_github_blueprint(client_id=GITHUB_CLIENT_ID,
                                         client_secret=GITHUB_CLIENT_SECRET)

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            account_image_url=account_info_json['login']
            avatarURL="https://avatars.githubusercontent.com/"
            profileURL=avatarURL+account_image_url
            return '<img src={profile}> <br> <h1>Hi  {name}'.format(profile=profileURL ,name=account_info_json['name'])

    return '<h1>Request failed!</h1>'

if __name__ == "__main__":
    app.run(debug=True)