import pytest
from model.InputParser import InputParser
from Queue import Queue
import pandas as pd
import numpy as np
import os


class TestCase(object):

    def getTestData(self, path):
        script_dir = os.path.dirname(__file__)
        file = os.path.join(script_dir, path)
        return pd.read_csv(file)

    def testShouldReturnExactOnePatientListAndEmptyCodeQueueList(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
        }
        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test1.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedPatients == {1: ['LAB']}

    def testShouldReturnExactTwoPatientListAndEmptyCodeQueueList(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
        }

        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test2.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedPatients == {1: ['LAB', 'XRAY']}

    def testShouldReturnNoPatientListAndOneCodeQueueList(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
        }
        codeInitialValue['XRAY'].put({1: ['LAB']})

        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test3.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'].get() == codeInitialValue['XRAY'].get()
        assert returnedPatients == {}

    def testShouldReturnOnePatientListAndOneCodeQueueList(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
        }
        codeInitialValue['LAB'].put({2: []})

        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test4.csv"))
        assert returnedCodeValues['LAB'].get() == codeInitialValue['LAB'].get()
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedPatients == {1: ['LAB']}

    def testShouldReturnNonePatientListAndNoneCodeQueueList(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
        }

        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test5.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedPatients == {}

    def testShouldReturnLAB_VISIT_2WHENPRESENTINQUEUE(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
            'LAB_VISIT_2': Queue()
        }

        codeInitialValue['LAB_VISIT_2'].put({1: 'LAB_VISIT_2'})
        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test6.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedCodeValues['LAB_VISIT_2'] == codeInitialValue['LAB_VISIT_2']
        assert returnedPatients == {}

    def testShouldNOTPUTINLAB_VISIT_2WHENCOMPLETED(self):
        codeInitialValue = {
            'LAB': Queue(),
            'XRAY': Queue(),
            'LAB_VISIT_2': Queue()
        }

        returnedCodeValues, returnedPatients = InputParser().processPatientList(codeInitialValue,
                                                                                self.getTestData("data/test7.csv"))
        assert returnedCodeValues['LAB'] == codeInitialValue['LAB']
        assert returnedCodeValues['XRAY'] == codeInitialValue['XRAY']
        assert returnedCodeValues['LAB_VISIT_2'] == codeInitialValue['LAB_VISIT_2']
        assert returnedPatients == {}
