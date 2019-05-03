class TimeKeeper:

    def __init__(self, patientManager):
        self.patientManager = patientManager

    def getTreshold(self):
        return self.patientManager.getTreshold()

    def getCompletedList(self):
        return self.patientManager.printResult()

    def predictTime(self):
        timeCounter = 0

        self.treshold = self.getTreshold()
        print(self.treshold)

        while (self.treshold is not None):
            timeCounter += self.treshold
            self.patientManager.completed(self.treshold, timeCounter)
            self.treshold = self.getTreshold()

        print(self.getCompletedList())
        print("success")
