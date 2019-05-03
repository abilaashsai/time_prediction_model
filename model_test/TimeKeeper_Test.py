from model.TimeKeeper import TimeKeeper
from model.PatientManager import PatientManager
from mock import Mock, patch


class TestCase(object):

    @patch('model.PatientManager.PatientManager.completed')
    def testShouldStopWhenInitialTresholdIsZero(self, patientManagerCompleted):
        timeKeeper = TimeKeeper(PatientManager)
        timeKeeper.getTreshold = Mock(return_value=None)
        timeKeeper.getCompletedList = Mock(return_value='hello')
        timeKeeper.predictTime()
        assert patientManagerCompleted.called == False

    @patch('model.PatientManager.PatientManager.completed')
    def testShouldStopWhenInitialTresholdIsZero(self, patientManagerCompleted):
        timeKeeper = TimeKeeper(PatientManager)
        timeKeeper.getTreshold = Mock()
        timeKeeper.getTreshold.side_effect = [5, None]
        timeKeeper.getCompletedList = Mock(return_value='hello')
        timeKeeper.predictTime()
        assert patientManagerCompleted.called == True
