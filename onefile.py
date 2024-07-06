import requests
from bs4 import BeautifulSoup

class OneFileTimesheetEntry:

    def __init__(self):
        categoryLabel = str()
        dateFromLabel = str()
        dateToLabel = str()
        titleLabel = str()
        timeLabel = str()

class OnefileClass:

    def __init__(self):
        self.session = requests.session()
        self.entries = list()

    def login(self,uname,pword):
        
        r = self.session.get("https://onefile.co.uk/")
        file = open("Results1_GetOnefile.txt",'w')
        file.write(r.text)
        file.close()

        r = self.session.get('https://login.onefile.co.uk/')
        file = open("Results2_GetLogin.txt",'w')
        file.write(r.text)
        file.close()
        for cookie in r.cookies:
            print(cookie)

        payload = {
            'email' : uname,
            'password' : pword
        }

        r = self.session.post('https://login.onefile.co.uk/api/authentication',json=payload)

        file = open("Results3_PostLogin.txt",'w')
        file.write(r.text)
        file.close()
        print(r.status_code)

        r = self.session.get('https://login.onefile.co.uk/api/user')
        for cookie in r.cookies:
            print(cookie)
        file = open("Results4_GetUser.txt",'w')
        file.write(r.text)
        file.close()
        print(r.status_code)
        for cookie in self.session.cookies:
            print(cookie)

        r = self.session.get("https://login.onefile.co.uk/api/keychain-account/login/478363")
        file = open("Results5_GetkeychainAccount.txt","w")
        file.write(r.text)
        file.close()
        for cookie in self.session.cookies:
            print(cookie)

        r = self.session.get("https://live.onefile.co.uk/learner/")
        file = open("Results6_GetLearner.txt","w")
        file.write(r.text)
        file.close()

    def getTimesheet(self):

        self.session.cookies.set('OneFilePageSize','1000')
        r = self.session.get("https://live.onefile.co.uk/timesheet/")
        file = open("Results7_GetTimesheets.txt","w")
        file.write(r.text)
        file.close()
        print("Cookies for timesheet:\n")
        for cookie in self.session.cookies:
            print(cookie)
        
        file = open("Results7_GetTimesheets.txt","r")
        for line in file:
            if 'CategoryLabel' in line:
                entry = OneFileTimesheetEntry()
                entry.categoryLabel = line.split('>')[1].split('<')[0]
                for line in file:
                    if 'DateFromLabel' in line:
                        entry.dateFromLabel = line.split('>')[1].split('<')[0]
                    elif 'DateToLabel' in line:
                        entry.dateToLabel = line.split('>')[1].split('<')[0]
                    elif 'CommentsLabel' in line:
                        entry.titleLabel = line.split('>')[1].split('<')[0]
                    elif 'TimeLabel' in line:
                        entry.timeLabel = line.split('>')[1].split('<')[0]
                        self.entries.append(entry)
                        break
        file.close()
        file = open("StructureLog.txt",'w')
        for entry in self.entries:
            file.write('    ' + entry.categoryLabel + '\n')
            file.write(entry.dateFromLabel + '\n')
            file.write(entry.dateToLabel + '\n')
            file.write(entry.titleLabel + '\n')
            file.write(entry.timeLabel + '\n')
                







    