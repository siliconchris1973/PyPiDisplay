from os import path

_cwd = path.dirname(path.abspath(__file__))
logindatasource = _cwd + path.sep + 'logindata'
validUser = ''
validPassword = ''

class userSession:
    def __init__(self):
        logondata = self.returnlogondata().split(':')
        self.validUser = logondata[0]
        self.validPassword = logondata[1]

    @staticmethod
    def returnlogondata():
        try:
            with open(logindatasource, 'r') as f:
                return f.read()
        except Exception as e:
            return str(e)

    def checklogin(self, username, password):
        if username == self.validUser and password == self.validPassword:
            return True
        else:
            return False
