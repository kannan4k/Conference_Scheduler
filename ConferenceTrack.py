#!/usr/bin/python
# By: Kannan Ponnusamy
import sys
import datetime as dt
from datetime import datetime
import time

class Session(object):
    """__init__() functions as the class constructor"""
    def __init__(self, fullTitle=None, title=None, talkTime=None):
        self.fullTitle = fullTitle
        self.title = title
        self.talkTime = talkTime
        self.scheduled = False;
        self.startTime=0;
        
        
class ConferenceTrack:

    def __init__(self):
        """ generated source for method __init__ """

    # Generic method to schedule conference track management
    def conferenceTrackSchedule(self, fileName):
        """ generated source for method conferenceTrackSchedule """
        talkList = self.getTalksFromInputFile(fileName)
        return self.conferenceTrackScheduleNext(talkList)
    
    def conferenceTrackScheduleNext(self, talkList):
        talkList = self.createTalks(talkList)
        return self.getScheduledConferenceTrack(talkList)
    
    def getTalksFromInputFile(self, fileName):
        # Reading the contents of the given input file
        try:
            talkList = []
            i=0
            f = open(fileName, 'rU')
            talkList = [line.rstrip('\n') for line in f]
            f.close()
        except IOError:
            print "File not available or error in read data"
            sys.exit(0)
        return talkList
    
    #Read the talks line by line and creating objects
    def createTalks(self, talkList):
        # If the talks list is empty it will throw the Exception
        if not talkList:
            print 'List is empty'
        temp=0
        validTalksList = []
        endWithMin = "min"
        endWithLightning = 'lightning'
        i=1
        for talk in talkList:
            #print talk
            lastWord = talk.rfind(" ")
            try:
                if lastWord == -1:
                    raise Exception(" Invalid talk ")
            except Exception:
                print "Invalid talk "
            title = talk[0:lastWord]
            timeInMin = talk[lastWord+1:].rstrip()
            
            
            # If title is missing or blank.
            try:
                if not title:
                    raise Exception('Invalid Name of the Talk')
                elif not timeInMin.endswith(endWithMin) and not timeInMin.endswith(endWithLightning): 
                    raise Exception('Invalid talk time please specify in minutes eg: 40min')
            except Exception as e:
                print e
                
            try:
                if timeInMin.endswith(endWithMin):
                    timeInMin.find(endWithMin)
                    time = int(timeInMin[0:timeInMin.find(endWithMin)])
                elif timeInMin.endswith(endWithLightning):
                    time =5
            except Exception as e:
                print e
            #print talk,title,time
            talkObject = Session(talk,title,time)
            validTalksList.append(talkObject)
        return validTalksList

    #To schedule the conference
    def getScheduledConferenceTrack(self,talkList):
        minTime = 6 * 60;
        sumOfTalkTime = self.getSumOfTalksTime(talkList);
        numberOfDays = sumOfTalkTime/minTime;
        
        allUnscheduledTalkList=[]
        allUnscheduledTalkList = list(talkList);
        allUnscheduledTalkList = sorted(talkList, key=lambda Session: Session.talkTime,reverse=True)
        talkListSize = len(allUnscheduledTalkList)
        morningSessions = self.calculateCombinations(allUnscheduledTalkList, numberOfDays, True);
        
        #Morning
        for talkList in morningSessions:
            for talk in talkList:
                allUnscheduledTalkList.remove(talk);
                
        # Evening
        eveningSessions = self.calculateCombinations(allUnscheduledTalkList, numberOfDays, False);
        
        # If a talk is scheduled in evening session remove from the existing list
        for talkList in eveningSessions:
            for talk in talkList:
                allUnscheduledTalkList.remove(talk);
        
        #print "Hello"
        #for i in allUnscheduledTalkList:
        #        print i.title
        #print "Hello"
        
        # If the list still has the values then we need to place it in evening session 
        maxTimeForASession = 240;
        if allUnscheduledTalkList:
            scheduledTalkList = []
            for talkList in eveningSessions:
                totalTime = self.getSumOfTalksTime(talkList);
                
                for talk in allUnscheduledTalkList:
                    talkTime = talk.talkTime;
                    if talkTime + totalTime <= maxTimeForASession:
                        talkList.append(talk)
                        talk.scheduled = True
                        scheduledTalkList.append(talk);
                for talk in scheduledTalkList:
                    allUnscheduledTalkList.remove(talk);
                if not allUnscheduledTalkList:
                    break
        
        # If list still not empty we have to throw error
        try:        
            if allUnscheduledTalkList:
                raise Exception("Can't schedule all tasks")
        except Exception:
                print "Can't schedule all tasksg" 
        
        return self.getScheduledTalksList(morningSessions, eveningSessions);
        
      
    #Display the Morning and Evening scheduled Talks:
    def getScheduledTalksList(self, morningSessions, eveningSessions):
        scheduledTalksList = []
        numberOfDays = len(morningSessions)
        for dayCount in range(numberOfDays):
            talkList=[]
            
            # Initialize the time to 9.00AM as the conference starts at that time
            time_string = '09:00 AM'
            format = '%I:%M %p'
            my_time = datetime.strptime(time_string, format)
            
            # This prints '1990-01-01 09.00 AM'
            scheduledTime = my_time.strftime(format)
            trackCount = dayCount + 1;
            print "Day ",trackCount 
            temp = 0
            # To display the morning sessions 
            mornSessionTalkList = morningSessions[dayCount];
            for talk in mornSessionTalkList:
                talk.startTime = my_time
                scheduledTime = my_time.strftime(format)
                print scheduledTime, talk.title
                my_time = my_time + dt.timedelta(minutes=talk.talkTime)
                temp +=talk.talkTime
                talkList.append(talk);
            #print my_time
            # Lunch time for 60mins
            lunchTimeDuration = 60;
            lunchTalk = Session("Lunch", "Lunch", 60);
            lunchTalk.startTime=my_time
            talkList.append(lunchTalk);
            
            scheduledTime = my_time.strftime(format)
            print scheduledTime, "Lunch Break"
            
            # To display the Evening sessions 
            my_time = my_time + dt.timedelta(minutes=lunchTimeDuration)
            eveSessionTalkList = eveningSessions[dayCount]
            for talk in eveSessionTalkList:
                talk.startTime = my_time
                talkList.append(talk);
                scheduledTime = my_time.strftime(format)
                print scheduledTime,talk.title
                my_time = my_time + dt.timedelta(minutes=talk.talkTime)
            
            
            # To display the Networking Event 
            networkingEvent = Session("Networking Event", "Networking Event", 60);
            networkingEvent.startTime = my_time
            talkList.append(networkingEvent);
            scheduledTime = my_time.strftime(format)
            print scheduledTime, "Networking Event\n"
            scheduledTalksList.append(talkList);
            my_time = my_time + dt.timedelta(minutes=talk.talkTime)
            
        
    # To FInd the possible combination of sessions
    def calculateCombinations(self,allUnscheduledTalkList,numberOfDays,morningSession):
        minTimeForASession = 180;
        maxTimeForASession = 240;
        if morningSession:
            maxTimeForASession = 180
        talkListSize = len(allUnscheduledTalkList)
        possibleTalksList = []
        possibleTalksListCount = 0;
        count = 0
        for count in range(talkListSize):
            anotherCount=count
            totalTime=0
            possibleCombinationList = []
            while anotherCount != talkListSize:
                currentCount = anotherCount;
                anotherCount+=1;
                currentTalk = allUnscheduledTalkList[currentCount];
                if currentTalk.scheduled:
                    continue;
                talkTime = currentTalk.talkTime;
                if talkTime > maxTimeForASession or talkTime + totalTime > maxTimeForASession:
                    continue;
                possibleCombinationList.append(currentTalk);
                totalTime += talkTime;
                if morningSession:
                    if totalTime == maxTimeForASession:
                        break;
                elif totalTime >= minTimeForASession:
                    break;
            count+=1
            
            
            sessionValid = False;
            if morningSession:
                sessionValid = (totalTime == maxTimeForASession);
            else:
                sessionValid = (totalTime >= minTimeForASession and totalTime <= maxTimeForASession);
                
            # Valid Session is when a combination matching the criteria of maxTimeForASession
            if sessionValid:
                possibleTalksList.append(possibleCombinationList);
                for talk in possibleCombinationList:
                    talk.scheduled = True
                possibleTalksListCount+=1;
                if possibleTalksListCount == numberOfDays:
                    break;
        return possibleTalksList
            
            
            
    # To return the total time of a object list
    def getSumOfTalksTime(self,talksList):
        if not talksList: 
            return 0
        totalTime = 0
        for talk in talksList:
            totalTime += talk.talkTime;
        return totalTime
    
    
#Main method      
def main():
    """ generated source for method main """
    import os
    filename = raw_input('Enter the input file path (eg: C:\Users\data.txt)::')
    #fileName = os.path.abspath(txtFilename)
    conferenceTrack = ConferenceTrack()
    conferenceTrack.conferenceTrackSchedule(filename)
    
if __name__ == '__main__':
    main()
