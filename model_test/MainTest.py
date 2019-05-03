from model import Main
from mock import Mock


class TestCase(object):
    def testShouldInitializeStationWithMockedData(self):
        Main.getStationData = Mock(return_value={
            'LAB': 6,
            'ECG': 8
        })
        stationQueue, stationWithTimeMap = Main.initializeStation()
        assert stationQueue['LAB'].empty() == True
        assert stationQueue['ECG'].empty() == True
        assert stationWithTimeMap['LAB'] == 6
        assert stationWithTimeMap['ECG'] == 8
