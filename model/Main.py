import os
import pandas as pd
from PatientManager import PatientManager
from TimeKeeper import TimeKeeper
from InputParser import InputParser

from Queue import Queue


def getDataSetTest():
    script_dir = os.path.dirname(__file__)
    file1 = os.path.join(script_dir, "data/test1.csv")
    return pd.read_csv(file1)


def getDataSet():
    script_dir = os.path.dirname(__file__)
    file1 = os.path.join(script_dir, "data/mhcqmsdata2017.csv")
    file2 = os.path.join(script_dir, "data/mhcqmsdata2018.csv")
    return pd.concat([pd.read_csv(file1), pd.read_csv(file2)])


def filterDataSet(data):
    removeIsPaused = data[data.isPaused == False]
    finalDataSet = removeIsPaused.drop(
        columns=['id', 'patientId', 'packageCode', 'coordinatorId', 'isPaused', 'pauseRemarks', 'details'])
    # remove if checkin is null and checkout is not null
    # rename lab visit 2 to LAB_VISIT_2
    return finalDataSet[finalDataSet.date >= '2018-05-31']


def getStationData():
    return {
        'LAB': 6,
        'XRAY': 12,
        'LAB_VISIT_1': 10,
        'BREAKFAST': 20
    }


def initializeStation():
    stationWithTimeMap = getStationData()

    stationQueue = {}
    for station in stationWithTimeMap:
        stationQueue[station] = Queue()
    return stationQueue, stationWithTimeMap


if __name__ == "__main__":
    # dataset = getDataSet()
    # filteredData = filterDataSet(dataset)

    filteredData = getDataSetTest()
    stationQueueInit, stationTimeMap = initializeStation()
    stationQueue, patientList = InputParser().processPatientList(stationQueueInit,
                                                                 filteredData)
    patientManager = PatientManager(stationQueue, patientList, stationTimeMap)
    timeKeeper = TimeKeeper(patientManager)

    predictTime = timeKeeper.predictTime()
