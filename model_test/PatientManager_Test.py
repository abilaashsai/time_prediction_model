from model.PatientManager import PatientManager
from Queue import Queue
from mock import Mock, patch


class TestCase(object):

    def testShouldNotSetInitialBreakFastTresholdWhenEmptyQueue(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {name: 20})
        assert (True if name not in patientManager.tempStationTreshold else False) == True
        assert (True if name not in patientManager.breakfast_lock else False) == True
        assert (True if name not in patientManager.breakfast else False) == True
        assert (True if name not in patientManager.stationQueue else False) == True
        assert patientManager.tempStationTreshold == {}

    def testShouldSetInitialBreakFastTreshold(self):
        name = 'BREAKFAST'
        breakfastQueue = Queue()
        patient = {1: [name, 'LAB']}
        breakfastQueue.put(patient)
        patientManager = PatientManager({name: breakfastQueue}, {}, {name: 10})
        assert patientManager.tempStationTreshold[name] == 10
        assert patientManager.breakfast_lock[1] == [name, 'LAB']
        assert patientManager.breakfast[1] == 10
        assert (True if name not in patientManager.stationQueue else False) == True
        assert patientManager.tempStationTreshold == {name: 10}

    def testShouldSetInitialBreakFastTresholdForMultiplePatient(self):
        name = 'BREAKFAST'
        breakfastQueue = Queue()
        patient1 = {1: [name, 'LAB']}
        patient2 = {2: [name, 'XRAY']}
        breakfastQueue.put(patient1)
        breakfastQueue.put(patient2)
        patientManager = PatientManager({name: breakfastQueue}, {}, {name: 50})
        assert patientManager.tempStationTreshold[name] == 50
        assert patientManager.breakfast_lock[1] == [name, 'LAB']
        assert patientManager.breakfast_lock[2] == [name, 'XRAY']
        assert patientManager.breakfast[1] == 50
        assert patientManager.breakfast[2] == 50
        assert (True if name not in patientManager.stationQueue else False) == True
        assert patientManager.tempStationTreshold == {name: 50}

    def testShouldReturnMinimumValueInList(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        assert patientManager.filterMin([9, 7, 6, 1, 5, 8, 5]) == 1
        assert patientManager.filterMin([9, 7, 6, 0, 5, 0, 1]) == 0
        assert patientManager.filterMin([6]) == 6
        assert patientManager.filterMin([]) == None

    def testShouldReturnTresholdforTimeValue(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        patientManager.tempStationTreshold = {'BREAKFAST': 17, 'ECG': 5}
        assert patientManager.getTreshold() == 5
        patientManager.tempStationTreshold = {'BREAKFAST': 17, 'ECG': 5, 'LAB': 1}
        assert patientManager.getTreshold() == 1

    def testShouldReturnKeyValueOfPatient(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        key, value = patientManager.getPatientKeyName({1: ['LAB', 'XRAY']})
        assert key == 1
        assert value == ['LAB', 'XRAY']

        key2, value2 = patientManager.getPatientKeyName({2: ['BREAKFAST']})
        assert key2 == 2
        assert value2 == ['BREAKFAST']

    def testShouldAddPatientToList(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        patientManager.addToPatientList(1, ['LAB'])
        patientManager.patientList = {1: ['LAB']}

    def testShouldAddPatientToListToNonEmptyDict(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {1: ['XRAY']}, {})
        patientManager.addToPatientList(3, ['ECG'])
        patientManager.patientList = {1: ['XRAY'], 3: ['ECG']}

    def testShouldNotAddPatientToListWhenNoValue(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        patientManager.addToPatientList(5, [])
        patientManager.patientList = {}

    def testShouldReturnFirstPatientFromPatientForStation(self):
        patientManager = PatientManager({'LAB': Queue(),
                                         'XRAY': Queue(), 'BREAKFAST': Queue()}, {1: ['LAB'], 2: ['LAB', 'XRAY']}, {})
        assert patientManager.patientList == {1: ['LAB'], 2: ['LAB', 'XRAY']}
        patient = patientManager.getPatientForStation('LAB')
        assert patient == {1: ['LAB']}
        assert patientManager.patientList == {2: ['LAB', 'XRAY']}

    def testShouldReturnFirstPatientFromPatientForStation2(self):
        patientManager = PatientManager({'LAB': Queue(),
                                         'XRAY': Queue(), 'BREAKFAST': Queue()}, {1: ['LAB'], 2: ['LAB', 'XRAY']}, {})
        assert patientManager.patientList == {1: ['LAB'], 2: ['LAB', 'XRAY']}
        patient = patientManager.getPatientForStation('XRAY')
        assert patient == {2: ['LAB', 'XRAY']}
        assert patientManager.patientList == {1: ['LAB']}

    def testShouldReturnNonePatientFromPatientForStation(self):
        patientManager = PatientManager({'LAB': Queue(),
                                         'XRAY': Queue(), 'BREAKFAST': Queue()}, {1: ['LAB'], 2: ['LAB', 'XRAY']}, {})
        assert patientManager.patientList == {1: ['LAB'], 2: ['LAB', 'XRAY']}
        patient = patientManager.getPatientForStation('ECG')
        assert patient == None
        assert patientManager.patientList == {1: ['LAB'], 2: ['LAB', 'XRAY']}

    def testShouldReDefineTresholdIfPresent(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {'BREAKFAST': 18, 'ECG': 5})
        patientManager.redefineTreshold('BREAKFAST', True)
        assert patientManager.tempStationTreshold['BREAKFAST'] == 18
        patientManager.redefineTreshold('ECG', True)
        assert patientManager.tempStationTreshold['ECG'] == 5

    def testShouldNotReDefineTresholdIfNotPresent(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        patientManager.redefineTreshold('BREAKFAST', False)
        assert (True if 'BREAKFAST' not in patientManager.tempStationTreshold else False) == True

    def testShouldNotReDefineTresholdIfNotPresentAndDeleteFromTreshold(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})
        patientManager.tempStationTreshold['BREAKFAST'] = 8
        assert (True if 'BREAKFAST' in patientManager.tempStationTreshold else False) == True
        patientManager.redefineTreshold('BREAKFAST', False)
        assert (True if 'BREAKFAST' not in patientManager.tempStationTreshold else False) == True

    @patch('model.PatientManager.PatientManager.redefineTreshold')
    def testShouldSchedulePatientsToEmptyStations(self, redefineTreshold):
        patientManager = PatientManager({'BREAKFAST': Queue(), 'LAB': Queue()}, {}, {})
        patientManager.getPatientForStation = Mock(return_value={1: ['LAB']})
        patientManager.schedulePatientsToEmptyStations()
        assert patientManager.stationQueue['LAB'].get() == {1: ['LAB']}
        assert redefineTreshold.called == True

    @patch('model.PatientManager.PatientManager.redefineTreshold')
    def testShouldNotSchedulePatientsToEmptyStations(self, redefineTreshold):
        patientManager = PatientManager({'BREAKFAST': Queue(), 'LAB': Queue()}, {}, {})
        patientManager.getPatientForStation = Mock(return_value=None)
        assert patientManager.stationQueue['LAB'].empty() == True
        patientManager.schedulePatientsToEmptyStations()
        assert patientManager.stationQueue['LAB'].empty() == True
        assert redefineTreshold.called == True

    def testShouldLogCompletedList(self):
        patientManager = PatientManager({'BREAKFAST': Queue()}, {}, {})

        assert (True if 1 not in patientManager.completedList else False) == True
        patientManager.logCompletedList('LAB', 1, 10)
        assert patientManager.completedList[1] == {'LAB': 10}
        patientManager.logCompletedList('XRAY', 1, 20)
        assert patientManager.completedList[1] == {'LAB': 10, 'XRAY': 20}

    def testShouldHandleBreakfastRequest(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {})
        patientManager.breakfast_lock[1] = ['LAB', 'XRAY', name]
        patientManager.breakfast[1] = 5
        patientManager.tempStationTreshold[name] = 5
        assert patientManager.tempStationTreshold[name] == 5
        assert patientManager.breakfast == {1: 5}
        assert patientManager.breakfast_lock == {1: ['LAB', 'XRAY', name]}
        patientManager.handleBreakfastRequest(name, 15)
        assert (True if name not in patientManager.tempStationTreshold else False) == True
        assert patientManager.breakfast == {}
        assert patientManager.breakfast_lock == {}

    def testShouldHandleBreakfastRequestForMultiplepatients(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {})
        patientManager.breakfast_lock[1] = ['LAB', 'XRAY', name]
        patientManager.breakfast[1] = 5
        patientManager.breakfast_lock[2] = ['LAB', 'ECG', name]
        patientManager.breakfast[2] = 10
        patientManager.breakfast_lock[3] = ['ECG', 'XRAY', name]
        patientManager.breakfast[3] = 5
        patientManager.tempStationTreshold[name] = 5
        assert patientManager.tempStationTreshold[name] == 5
        assert patientManager.breakfast == {1: 5, 2: 10, 3: 5}
        assert patientManager.breakfast_lock == {1: ['LAB', 'XRAY', name], 2: ['LAB', 'ECG', name],
                                                 3: ['ECG', 'XRAY', name]}
        patientManager.handleBreakfastRequest(name, 15)
        assert patientManager.tempStationTreshold[name] == 5
        assert patientManager.breakfast == {2: 5}
        assert patientManager.breakfast_lock == {2: ['LAB', 'ECG', name]}
        assert patientManager.patientList == {1: ['LAB', 'XRAY'], 3: ['ECG', 'XRAY']}

    def testShouldAddPatientToBreakfastList(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {name: 20})
        patientManager.addToBreakfastList(name, 1, ['LAB', 'XRAY'])
        assert patientManager.breakfast_lock[1] == ['LAB', 'XRAY']
        assert patientManager.breakfast[1] == 20

    def testShouldReturnStationWithZeroTreshold(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {})
        patientManager.tempStationTreshold = {'LAB': 0, 'XRAY': 10, 'ECG': 0}
        assert patientManager.getStationWithTresholdZero() == ['ECG', 'LAB']

    def testShouldReCalculateTreshold(self):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {})
        patientManager.tempStationTreshold = {'LAB': 5, 'XRAY': 7, 'ECG': 18}
        patientManager.reCalculateTreshold(5)
        assert patientManager.tempStationTreshold == {'LAB': 0, 'XRAY': 2, 'ECG': 13}

    @patch('model.PatientManager.PatientManager.schedulePatientsToEmptyStations')
    @patch('model.PatientManager.PatientManager.logCompletedList')
    @patch('model.PatientManager.PatientManager.addToBreakfastList')
    @patch('model.PatientManager.PatientManager.reCalculateTreshold')
    def testShouldCallLAB_VISIT_1Completed(self, reCalculateTreshold, addToBreakfastList, logCompletedList,
                                           schedulePatientsToEmptyStations):
        name = 'BREAKFAST'
        lab_visit = 'LAB_VISIT_1'
        patientManager = PatientManager({name: Queue(), lab_visit: Queue()}, {}, {})
        patientManager.getStationWithTresholdZero = Mock(return_value=[lab_visit])
        patientManager.stationQueue[lab_visit].put({1: ['LAB', lab_visit]})
        patientManager.completed(5, 10)
        assert reCalculateTreshold.called == True
        assert addToBreakfastList.called == True
        assert logCompletedList.called == True
        assert schedulePatientsToEmptyStations.called == True

    @patch('model.PatientManager.PatientManager.handleBreakfastRequest')
    @patch('model.PatientManager.PatientManager.reCalculateTreshold')
    def testShouldCallBreakfastCompleted(self, reCalculateTreshold, addToBreakfastList):
        name = 'BREAKFAST'
        patientManager = PatientManager({name: Queue()}, {}, {})
        patientManager.getStationWithTresholdZero = Mock(return_value=[name])
        patientManager.completed(5, 10)
        assert reCalculateTreshold.called == True
        assert addToBreakfastList.called == True

    @patch('model.PatientManager.PatientManager.schedulePatientsToEmptyStations')
    @patch('model.PatientManager.PatientManager.logCompletedList')
    @patch('model.PatientManager.PatientManager.addToPatientList')
    @patch('model.PatientManager.PatientManager.reCalculateTreshold')
    def testShouldCallLAB_VISIT_1Completed(self, reCalculateTreshold, addToPatientList, logCompletedList,
                                           schedulePatientsToEmptyStations):
        name = 'BREAKFAST'
        ecg = 'ECG'
        patientManager = PatientManager({name: Queue(), ecg: Queue()}, {}, {})
        patientManager.getStationWithTresholdZero = Mock(return_value=[ecg])
        patientManager.stationQueue[ecg].put({1: ['LAB', ecg]})
        patientManager.completed(5, 10)
        assert reCalculateTreshold.called == True
        assert addToPatientList.called == True
        assert logCompletedList.called == True
        assert schedulePatientsToEmptyStations.called == True
