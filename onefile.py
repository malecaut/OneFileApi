import requests
#from bs4 import BeautifulSoup
import json

class OneFileTimesheetEntry:

    def __init__(self):
        self.categoryLabel = str()

        self.dateFromLabel = str()
        self.dateToLabel = str()
        self.timeFromLabel = str()
        self.timeToLabel = str()
        self.dateCreated = str()
        self.timeCreated = str()

        self.titleLabel = str()
        self.timeLabel = str()

        self.timesheetId = str()
        self.isOTJ = str()
        self.timeSheetCategoryId = str()

        self.textData = str()
        self.trainingActivities = list()
        self.criteria = list()
        self.files = list()
        self.linkedActivityId = str()

        self.someID = str()

class OnefileCriteria:

    def __init__(self):
        self.unitID = str()
        self.unitTitle = str()
        self.sectionHeading = str()
        self.criteriaID = str()
        self.criteriaReference = str()
        self.criteriaTitle = str()
        



class OnefileClass:

    def __init__(self):
        self.keychainAccountId = str()
        self.productUserId = str()

        self.session = requests.session()

        self.entries = list()
        self.journalCategories = dict()
        self.entryCounter = int()

        self.criteriaDict = dict()

        self.standardID = str()
        self.standardTitle = str()

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
        self.entryCounter= 0 
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
                        self.entryCounter = self.entryCounter + 1
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
            entry = OneFileTimesheetEntry()
            entry.timesheetId = str(journalJson['timesheetID'])
            entry.dateFromLabel = journalJson['dateFrom'][0:9]
            entry.timeFromLabel = journalJson['dateFrom'].split('T')[1][0:7]
            entry.dateToLabel = journalJson['dateTo'][0:9]
            entry.timeToLabel = journalJson['dateTo'].split('T')[1][0:7]
            entry.dateCreated = journalJson['dateTimesheet'][0:9]
            entry.timeCreated = journalJson['dateTimesheet'].split('T')[1][0:7]
            entry.titleLabel = journalJson['comments']
            entry.timeLabel = str(journalJson['time'])
            entry.isOTJ = str(journalJson['isOffTheJob'])
            entry.timeSheetCategoryId = str(journalJson['timeSheetCategoryID'])
            self.entries.append(entry)
        
        r = self.session.get("https://learning.onefile.co.uk/api/trainingactivity/category")
        categories = json.loads(r.text)
        for category in categories:
            self.journalCategories[str(category['timesheetCategoryID'])] = category['timesheetCategory']

        for entry in self.entries:
            entry.categoryLabel = self.journalCategories[entry.timeSheetCategoryId]


        r = self.session.get("https://learning.onefile.co.uk/api/journalEntry")
        file = open("Results9_GetJournalDetailed.txt",'w')
        file.write(r.text)

        data = json.loads(r.text)
        lastDate = str()

        counter = 0
        while data:
            for journalJson in data:
                lastDate = str(journalJson['createdOn'])[0:19]
                found = False
                for entry in self.entries:
                    if entry.timesheetId == str(journalJson['linkedActivityId']).strip():
                        counter = counter + 1
                        found = True
                        entry.textData = journalJson['entryData']['text']
                        if entry.textData == "":
                            entry.textData = "You added no comments"
                        for activity in journalJson['entryData']['trainingActivities']:
                            entry.trainingActivities.append(str(activity))
                        if journalJson['entryData']['criteria']:
                            for criteria in journalJson['entryData']['criteria']:
                                entry.criteria.append(str(criteria))
                        if journalJson['entryData']['files']:
                            for afile in journalJson['entryData']['files']:
                                entry.files.append(str(afile))
                        entry.linkedActivityId = str(journalJson['linkedActivityId']).strip()
                        entry.someID = str(journalJson['id'])
                        break
                if found == False:
                    print(str(journalJson['entryData']['trainingActivities'][0]))
            rParams = {
                'lastEntryDate' : lastDate
            }
            r = self.session.get("https://learning.onefile.co.uk/api/journalEntry?lastEntryDate=" + lastDate)
            file.write(r.text)

            print(r.status_code)
            print(lastDate)
            data = json.loads(r.text)
        file.close()
        print(counter)    
        print(self.entryCounter)

        print(self.entries[0].someID)
        r = self.session.post("https://learning.onefile.co.uk/api/standard/getJournalStandards",json=self.entries[0].someID)
        print(r.status_code)
        file = open("Results10_getJournalStandard.txt",'w')
        file.write(r.text)
        file.close()
        data = json.loads(r.text)
        data = data[0]
        self.standardID = str(data['standard_id'])
        self.standardTitle = data['title']

        for unit in data['requirements']:
            unitID = unit['unit_id']
            unitTitle = unit['title']
            for section in unit['sections']:
                sectionHeading = section['heading']
                for criteria in section['criteria']:
                    newCriteria = OnefileCriteria()
                    newCriteria.criteriaID = str(criteria['criteria_id'])
                    newCriteria.criteriaReference = criteria['criteria_reference']
                    newCriteria.criteriaTitle = criteria['text']
                    newCriteria.sectionHeading = sectionHeading
                    newCriteria.unitID = unitID
                    newCriteria.unitTitle = unitTitle
                    self.criteriaDict[newCriteria.criteriaID] = newCriteria
        



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
            file.write("Description: " + entry.textData + '\n')
            file.write("Training Activities: " + '\n')
            for activity in entry.trainingActivities:
                file.write('\t' + activity + '\n')
            file.write("Criteria: " + '\n')
            for criteria in entry.criteria:
                file.write('\t' + str(criteria) + ' ' + self.criteriaDict[criteria].criteriaTitle + '\n')
            file.write("Linked Files: " + '\n')
            for line in entry.files:
                file.write('\t' + line + '\n')
            file.write("Linked activity: " + entry.linkedActivityId + '\n')
        file.close()







    