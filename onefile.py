import requests
from bs4 import BeautifulSoup

class OnefileClass:

    def login(self,uname,pword):
        with requests.session() as s:
            r = s.get("https://onefile.co.uk/")
            file = open("Results_GetOnefile.txt",'w')
            file.write(r.text)
            file.close()

            r = s.get('https://login.onefile.co.uk/')
            file = open("Results_GetLogin.txt",'w')
            file.write(r.text)
            file.close()
            for cookie in r.cookies:
                print(cookie)

            payload = {
                'email' : uname,
                'password' : pword
            }

            r = s.post('https://login.onefile.co.uk/api/authentication',json=payload)

            file = open("Results_PostLogin.txt",'w')
            file.write(r.text)
            file.close()
            print(r.status_code)

            r = s.get('https://login.onefile.co.uk/api/user')
            file = open("Results_GetUser.txt",'w')
            file.write(r.text)
            file.close()
            print(r.status_code)

