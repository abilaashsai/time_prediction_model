import collections


class PatientManager:

    def getPatientKeyName(self, patient):
        return patient.keys()[0], patient.values()[0]

    def setInitialBreakfastTreshold(self, name):
        while not self.stationQueue[name].empty():
            patient = self.stationQueue[name].get()
            pKey, pValue = self.getPatientKeyName(patient)
            self.breakfast_lock[pKey] = pValue
            self.breakfast[pKey] = self.stationTimeMap[name]

        del self.stationQueue[name]

    def setInitialStationTreshold(self):
        for key in self.stationQueue:
            if not self.stationQueue[key].empty():
                self.tempStationTreshold[key] = self.stationTimeMap[key]

    def __init__(self, stationQueue, patientList, stationTimeMap):
        self.stationQueue = stationQueue
        self.patientList = patientList
        self.stationTimeMap = stationTimeMap
        self.tempStationTreshold = {}
        self.completedList = {}

        self.breakfast = {}
        self.breakfast_lock = {}
        self.setInitialStationTreshold()
        self.setInitialBreakfastTreshold('BREAKFAST')

    def filterMin(self, listValue):
        if listValue:
            return reduce((lambda x, y: x if x <= y else y), listValue)
        return None

    def addToPatientList(self, pKey, pValue):
        if pValue:
            self.patientList[pKey] = pValue

    def getPatientForStation(self, name):
        sortedList = collections.OrderedDict(sorted(sorted(self.patientList.items())))

        for i, (key, value) in enumerate(sortedList.iteritems()):
            if name in value:
                patient = {key: self.patientList[key]}
                del self.patientList[key]
                return patient
        return None

    def redefineTreshold(self, station, isPresent):
        if isPresent:
            self.tempStationTreshold[station] = self.stationTimeMap[station]
        else:
            if station in self.tempStationTreshold:
                del self.tempStationTreshold[station]

    def schedulePatientsToEmptyStations(self):
        emptyStations = [key for key in self.stationQueue if
                         self.stationQueue[key].empty()]

        for station in emptyStations:
            patient = self.getPatientForStation(station)
            if patient:
                self.stationQueue[station].put(patient)
            self.redefineTreshold(station, patient is not None)

    def getTreshold(self):
        self.schedulePatientsToEmptyStations()
        return self.filterMin(map(lambda key: self.tempStationTreshold[key], self.tempStationTreshold))

    def logCompletedList(self, name, pKey, time):
        if pKey not in self.completedList:
            self.completedList[pKey] = {}
        self.completedList[pKey][name] = time

    def handleBreakfastRequest(self, name, treshold, time):
        keyStore = []
        for key in self.breakfast:
            self.breakfast[key] -= treshold
            if self.breakfast[key] is 0:
                self.breakfast_lock[key].remove(name)
                self.addToPatientList(key, self.breakfast_lock[key])
                self.logCompletedList(name, key, time)
                keyStore.append(key)

        for key in keyStore:
            del self.breakfast_lock[key]
            del self.breakfast[key]

        if not self.breakfast:
            del self.tempStationTreshold['BREAKFAST']
        else:
            minValue2 = self.filterMin([self.breakfast[key] for key in self.breakfast])
            self.tempStationTreshold[name] = minValue2

    def addToBreakfastList(self, name, pKey, pValue):
        if pValue:
            self.breakfast_lock[pKey] = pValue
            self.breakfast[pKey] = self.stationTimeMap['BREAKFAST']
            if 'BREAKFAST' not in self.tempStationTreshold:
                self.tempStationTreshold['BREAKFAST'] = self.stationTimeMap['BREAKFAST']

            if not self.stationQueue[name].empty():
                self.tempStationTreshold[name] = self.stationTimeMap[name]

    def getStationWithTresholdZero(self):
        return filter(lambda x: self.tempStationTreshold[x] is 0, self.tempStationTreshold)

    def reCalculateTreshold(self, treshold, time):

        for key in self.tempStationTreshold:
            self.tempStationTreshold[key] -= treshold
        if self.breakfast:
            self.handleBreakfastRequest('BREAKFAST', treshold, time)

    def doNone(self):
        print("hello")

    def completed(self, treshold, time):
        self.reCalculateTreshold(treshold, time)

        for name in self.getStationWithTresholdZero():
            if name == 'LAB_VISIT_1':
                pKey, pValue = self.getPatientKeyName(self.stationQueue[name].get())
                pValue.remove(name)
                self.addToBreakfastList(name, pKey, pValue)
                self.logCompletedList(name, pKey, time)

            elif name == 'BREAKFAST':
                self.doNone()
            else:
                pKey, pValue = self.getPatientKeyName(self.stationQueue[name].get())
                pValue.remove(name)
                self.addToPatientList(pKey, pValue)
                self.logCompletedList(name, pKey, time)

    def printResult(self):
        return self.completedList
