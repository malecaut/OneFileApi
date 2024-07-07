import requests
from bs4 import BeautifulSoup
import json

class OneFileTimesheetEntry:

    def __init__(self):
        self.categoryLabel = str()
        self.dateFromLabel = str()
        self.dateToLabel = str()
        self.titleLabel = str()
        self.timeLabel = str()
        self.createdOnLabel = str()
        self.timesheetId = str()
        self.isOTJ = str()
        self.timeSheetCategoryId = str()
        self.textData = str()
        self.trainingActivities = list()
        self.criteria = list()
        self.files = list()
        self.linkedActivityId = str()



class OnefileClass:

    def __init__(self):
        self.keychainAccountId = str()
        self.productUserId = str()

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
        data = json.loads(r.text)
        self.keychainAccountId = str(data["accounts"][0]["keychainAccountId"])
        self.productUserId = str(data["accounts"][0]["productUserId"])
        print(self.keychainAccountId)
        print(self.productUserId)

        r = self.session.get("https://login.onefile.co.uk/api/keychain-account/login/" + self.keychainAccountId)
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
        file.close()
                
    def getJournal(self):
        r = self.session.get("https://learning.onefile.co.uk/api/trainingactivity",params=self.productUserId)
        file = open("Results8_GetJournal.txt",'w')
        file.write(r.text)
        file.close()
        data = json.loads(r.text)
        for journalJson in data:
            for entry in self.entries:
                if entry.titleLabel == journalJson['comments']:
                    entry.timesheetId = str(journalJson['timesheetID'])
                    entry.isOTJ = str(journalJson['isOffTheJob'])
                    entry.timeSheetCategoryId = str(journalJson['timeSheetCategoryID'])
                    entry.createdOnLabel = str(journalJson['dateTimesheet'][0:16])
        
        file = open("StructureLog.txt",'w')
        for entry in self.entries:
            file.write('    ' + entry.categoryLabel + '\n')
            file.write(entry.dateFromLabel + '\n')
            file.write(entry.dateToLabel + '\n')
            file.write(entry.titleLabel + '\n')
            file.write(entry.timeLabel + '\n')
            file.write(entry.timesheetId + '\n')
            file.write(entry.isOTJ + '\n')
            file.write(entry.timeSheetCategoryId + '\n')
            file.write(entry.createdOnLabel + '\n')
        file.close()

        r = self.session.get("https://learning.onefile.co.uk/api/journalEntry")
        file = open("Results9_GetJournalDetailed.txt",'w')
        file.write(r.text)
        file.close()

        data = json.loads(r.text)
        for journalJson in data:
            for entry in self.entries:
                if entry.createdOnLabel == journalJson['createdOn'][0:16]:
                    entry.textData = journalJson['entryData']['text']
                    if entry.textData == "":
                        entry.textData = "You added no comments"
                    #entry.trainingActivities = str(journalJson['entryData']['trainingActivities'])
                    for activity in journalJson['entryData']['trainingActivities']:
                        entry.trainingActivities.append(str(activity))
                    #entry.trainingActivities = [str(activityId) for activityId in journalJson['entryData']['trainingActivities']]
                    for criteria in journalJson['entryData']['criteria']:
                        entry.criteria.append(criteria)
                    #entry.criteria = str(journalJson['entryData']['criteria'])
                    #entry.files = str(journalJson['entryData']['files'])
                    #if journalJson['entryData']['files']:
                        #entry.files = [str(file_id) for file_id in journalJson['entryData']['files']]
                    #else:
                        #entry.files.append("")
                    if journalJson['entryData']['files']:
                        for afile in journalJson['entryData']['files']:
                            entry.files.append(str(afile))
                        entry.linkedActivityId = str(journalJson['linkedActivityId'])
                    #for activity in journalJson['linkedActivityId']:
                        #entry.linkedActivityId.append(activity)
                    #entry.linkedActivityId = [str(activityId) for activityId in journalJson['linkedActivityId']]

                    break
                                        

        file = open("StructureLog.txt",'w')
        for entry in self.entries:
            file.write('\n\t\t' + entry.categoryLabel + '\n')
            file.write("Date from: " + entry.dateFromLabel + '\n')
            file.write("Date to: " + entry.dateToLabel + '\n')
            file.write("Title: " + entry.titleLabel + '\n')
            file.write("Time: " + entry.timeLabel + '\n')
            file.write("Timesheet id: " + entry.timesheetId + '\n')
            file.write("OTJ: " + entry.isOTJ + '\n')
            file.write("Timesheet category id: " + entry.timeSheetCategoryId + '\n')
            file.write("Date created: " + entry.createdOnLabel + '\n')
            file.write("Description: " + entry.textData + '\n')
            #for line in entry.trainingActivities:
                #file.write(line + '\n')
            #file.write("Training activity: " + entry.trainingActivities + '\n')
            file.write("Training Activities: " + '\n')
            for activity in entry.trainingActivities:
                file.write('\t' + activity + '\n')
            #file.write(entry.criteria)
            file.write("Criteria: " + '\n')
            for criteria in entry.criteria:
                file.write('\t' + str(criteria) + '\n')
            file.write("Linked Files: " + '\n')
            for line in entry.files:
                file.write('\t' + line + '\n')
            file.write("Linked activity: " + entry.linkedActivityId + '\n')
        file.close()







    