import bottle
from beaker.middleware import SessionMiddleware
import json
import redis
import os
import hashlib
import random
import smtplib

from config import config
config['sitewide']['site_url'] = config['site_url']

def hash_pw(password):
    return hashlib.md5(str(password)).hexdigest()

r = redis.StrictRedis(host=config['redis_location'], port=6379, db=0)

bottle.TEMPLATE_PATH.append('./templates')
app = bottle.app()

auth_secret = hash_pw(str(random.random()))

# helper functions
def send_emails(maildata, service='mock'):
    if service == 'mock':
        for data in maildata:
            print data
    elif service == 'gmail':
        # gmail doesn't allow From spoofing, so you may only send as this account
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(config['gmail_account'], config['gmail_password'])
        for data in maildata:
            server.sendmail(*data)
        server.close()
    else:
        raise NotImplemented('Need other mailers')

def make_mail(email, subject, body):
    source = config['sitewide']['couple']
    message = """\From: {}\nTo: {}\nSubject: {}\n\n{}
    """.format(source, email, subject, body)
    return (source, email, message)

def check_auth(key=None, return_falsy=False):
    """ key is the email or db key. if False, use session auth only, else check email field
        return_falsy returns False, else 401
    """
    s = bottle.request.environ.get('beaker.session')
    authenticated = s.get('authenticated')
    if key is None:
        key = bottle.request.forms.get('email')
    if authenticated and not key:
        return authenticated
    password = bottle.request.forms.get('password')
    hashed = r.hget(key, 'password')
    if key and password and (hash_pw(password) == hashed):
        s['authenticated'] = key
        return key
    if return_falsy:
        return False
    bottle.abort(401, 'wrong username or password')
    
# unauthenticated static content
@app.route('/static/<filename>')
def static(filename):
    return bottle.static_file(filename, root='./static')

# user registration and authentication (AAA ?) API
@app.route('/register', method='POST')
def register():
    s = bottle.request.environ.get('beaker.session')
    key = bottle.request.forms.get('email')
    password = bottle.request.forms.get('password')
    if r.exists(key):
        bottle.abort(401, 'email address already registered')
    else:
        m = make_mail(key, "Registered to {}".format(config['site_url']), "{} \n\n has been registered at \n\n {}".format(key, config['site_url']))
        send_emails([m])
        r.hset(key, 'password', hash_pw(password))
        s['authenticated'] = key
        bottle.redirect('/welcome')

@app.route('/authenticate', method='POST')
def authenticate():
    check_auth()
    bottle.redirect('/welcome')

@app.route('/unauthenticate', method='POST')
def unauthenticate():
    s = bottle.request.environ.get('beaker.session')
    s['authenticated'] = False
    bottle.redirect('/welcome')

@app.route('/password_reset', method='POST')
def password_reset():
    # create a key for two-factor auth
    key = bottle.request.forms.get('email')
    hashed = hash_pw(random.random())[:7]
    r.setex(hashed, 300, key)
    s = bottle.request.environ.get('beaker.session')
    s['authenticated'] = False
    m = make_mail(key, "Password recovery for {}".format(config['site_url']), "{} \n\n recovery key \n\n {}".format(key, hashed))
    send_emails([m])
    bottle.redirect('/recover')

@app.route('/change_email', method='POST')
def change_email():
    # everything is keyed off email address, so changing it is a bit of a pain
    key = bottle.request.forms.get('new_email')
    old_email = check_auth()
    if r.exists(key):
        bottle.abort(401, 'email address already registered')
    data = r.hgetall(old_email)
    r.hmset(key, data)
    r.delete(old_email)
    s = bottle.request.environ.get('beaker.session')
    s['authenticated'] = key
    bottle.redirect('/welcome')

@app.route('/reregister', method='POST')
def reregister():
    """ anything involving changing the password """
    key = bottle.request.forms.get('email')
    password = bottle.request.forms.get('password')
    secret = bottle.request.forms.get('secret')
    stored_key = r.get(secret)
    if key==check_auth(False, True) or (stored_key and stored_key==key):
        m = make_mail(key, "Password reset at {}".format(config['site_url']), "{} \n\n password was just reset at \n\n {}".format(key, config['site_url']))
        send_emails([m])
        r.hset(key, 'password', hash_pw(password))
        s = bottle.request.environ.get('beaker.session')
        s['authenticated'] = key
        bottle.redirect('/welcome')
    else:
        bottle.abort(401, 'wrong email address or your token expired')

# unauthenticated pages
@app.route('/')
@app.route('/welcome')
def index():
    data = {'authenticated': bool(check_auth(return_falsy=True))}
    data.update(config['sitewide'])
    return bottle.template('welcome', data)

@app.route('/recover')
def index():
    data = {'authenticated': bool(check_auth(return_falsy=True))}
    data.update(config['sitewide'])
    return bottle.template('recover', config['sitewide'])

# all authenticated pages
@app.route('/rsvp/submit', method='POST')
def index(name=None):
    key = check_auth()
    j = json.dumps(bottle.request.forms.dict)
    r.hset(key, 'rsvp', j)
    bottle.redirect('/rsvp')

@app.route('/rsvp')
def edit_rsvp(name=None):
    key = check_auth()
    d = r.hget(key, 'rsvp')
    j = json.loads(d) if d else {}
    j.update(config['sitewide'])
    return bottle.template('rsvp', j)

@app.route('/<name>')
def index(name=None):
    data = {'authenticated': bool(check_auth())}
    data.update(config['sitewide'])
    return bottle.template(name if name else 'welcome', data)

app = SessionMiddleware(app, {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.cookie_expires': 172800,
    'session.auto': True,
})
bottle.run(app=app, host=config['serve_from'], port=80, server='cherrypy', debug=True, reloader=True)