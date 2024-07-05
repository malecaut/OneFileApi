import requests
from bs4 import BeautifulSoup

class OnefileClass:

    def __init__(self):
        self.session = requests.session()

    def login(self,uname,pword):
        r = self.session.get("https://onefile.co.uk/")
        file = open("Results_GetOnefile.txt",'w')
        file.write(r.text)
        file.close()

        r = self.session.get('https://login.onefile.co.uk/')
        file = open("Results_GetLogin.txt",'w')
        file.write(r.text)
        file.close()
        for cookie in r.cookies:
            print(cookie)

        payload = {
            'email' : uname,
            'password' : pword
        }

        r = self.session.post('https://login.onefile.co.uk/api/authentication',json=payload)

        file = open("Results_PostLogin.txt",'w')
        file.write(r.text)
        file.close()
        print(r.status_code)

        r = self.session.get('https://login.onefile.co.uk/api/user')
        file = open("Results_GetUser.txt",'w')
        file.write(r.text)
        file.close()
        print(r.status_code)

