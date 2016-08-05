import sys
import logging
from logging.handlers import RotatingFileHandler

# to change the display implementation you only need to change the import here.
#from ShowStuff import Nokia5110 as Display
from ShowStuff import DummyDisplay as Display

from flask import Flask
from flask import render_template
from flask import session
import sys

app = Flask(__name__, template_folder='templates')
app.secret_key = '1VerySecretKey!'

display = Display.Display()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    if session.get('user'):
        return render_template('status.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/signin')
def help():
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/help')
def showhelp():
    return render_template('help.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

    except Exception as e:
        return render_template('error.html',error = str(e))

    if len(data) > 0:
        if check_password_hash(str(data[0][3]),_password):
            session['user'] = data[0][0]
            return redirect('/status')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
    else:
        return render_template('error.html',error = 'Wrong Email address or Password.')

def main():
    handler = RotatingFileHandler('/var/tmp/PyPiDisplay.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    appDebug=False

    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--server'):
            pass
        elif (sys.argv[1] == '--debug'):
            appDebug = True
        else:
            print('running all in console mode - please use --server to start a background server')
    else:
        print('running all in console mode and with debugging on - please use --server to start a background server')
        appDebug = True

    app.run(host='0.0.0.0', debug=appDebug)


if __name__ == '__main__':
    app.run()
