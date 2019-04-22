from flask import Blueprint, jsonify, request, abort, render_template, \
            session, redirect,  url_for, session, g, flash, render_template
from flask_cors import CORS, cross_origin

import requests


bp = Blueprint('oauth', __name__, url_prefix='/oauth')
CORS(bp, max_age=30*86400)

@bp.route('/login', methods=['GET'])
def google_login():
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = '1081117001308-6vqhk9191m88kmbvvdl2elmicm7fm923.apps.googleusercontent.com'
    redirect_uri = "http://localhost:5000/oauth/login/google/auth"
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri = token_request_uri,
        response_type = response_type,
        client_id = client_id,
        redirect_uri = redirect_uri,
        scope = scope)
    return redirect(url)

@bp.route('/login/google/auth', methods=['GET'])
def google_authenticate():
    # parser = Http()
    login_failed_url = 'http://localhost:5000/'
    # if 'error' in request.GET or 'code' not in request.GET:
    #     # return HttpResponseRedirect('{loginfailed}'.format(loginfailed = login_failed_url))
    #     return jsonify('Error while login')
    data = request.get_json()
    print("DATA", data)

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = "http://localhost:5000/oauth/login/google/auth"
    # params = urllib.urlencode({
    #     'code':request.GET['code'],
    #     'redirect_uri':redirect_uri,
    #     'client_id':'1081117001308-6vqhk9191m88kmbvvdl2elmicm7fm923.apps.googleusercontent.com',
    #     'client_secret':'KwafmS-_jJGixNW6_amLaK3k',
    #     'grant_type':'authorization_code'
    # })
    params = {
        'code':'code', #request.get('response_type'),
        'redirect_uri':redirect_uri,
        'client_id':'1081117001308-6vqhk9191m88kmbvvdl2elmicm7fm923.apps.googleusercontent.com',
        'client_secret':'KwafmS-_jJGixNW6_amLaK3k',
        'grant_type':'authorization_code'
    }
    headers={'content-type':'application/x-www-form-urlencoded'}
    # resp, content = parser.request(access_token_uri, method = 'POST', body = params, headers = headers)
    resp = requests.post(access_token_uri, data = params, headers = headers)
    print("RESP  ", resp)
    print(resp.content)
    # token_data = jsonDecode(content)
    # # resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken=token_data['access_token']))
    # resp = request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken=token_data['access_token']))
    # #this gets the google profile!!
    # google_profile = jsonDecode(content)
    # #log the user in-->
    # #HERE YOU LOG THE USER IN, OR ANYTHING ELSE YOU WANT
    # #THEN REDIRECT TO PROTECTED PAGE
    # for k, v in google_profile.items():
    #     print(k, v)
    # return jsonify(google_profile)

    # return HttpResponseRedirect('/dashboard')

@bp.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('oauth.google_login'))
    
    access_token = access_token[0]
    
    return render_template('index.html')
 
# @bp.route('/login')
# def login():
#     return twitter.authorize(callback=url_for('oauth_authorized',
#     next=request.args.get('next') or request.referrer or None))
 
# # @bp.route('/logout')
# # def logout():
# #     session.pop('screen_name', None)
# #     flash('You were signed out')
# # return redirect(request.referrer or url_for('index'))
 
# @bp.route('/oauth-authorized')
# @twitter.authorized_handler
# def oauth_authorized(resp):
#     next_url = request.args.get('next') or url_for('index')
#     if resp is None:
#         flash(u'You denied the request to sign in.')
#     return redirect(next_url)
 
#     access_token = resp['oauth_token']
#     session['access_token'] = access_token
#     session['screen_name'] = resp['screen_name']
    
#     session['twitter_token'] = (
#         resp['oauth_token'],
#         resp['oauth_token_secret']
#     )
    
#     return redirect(url_for('index'))