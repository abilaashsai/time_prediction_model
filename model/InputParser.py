import json


class InputParser:

    def processPatientList(self, codeQueuelist, data):
        self.patientInqueue = {}
        self.codeQueuelist = codeQueuelist

        def parseData(rowValue):
            station_data = json.loads(rowValue['stations'])
            patientCodeList = []
            assignStation = ""

            for station in station_data:
                if not station['isRemoved']:
                    if not station['checkin'] and not station['checkout']:
                        if str(station['code']) == 'LAB_VISIT_1':
                            assignStation = station['code']
                            patientCodeList.append(str(station['code']))
                        else:
                            patientCodeList.append(str(station['code']))
                    elif station['checkin'] and not station['checkout']:
                        assignStation = station['code']
                        patientCodeList.append(str(station['code']))

            if patientCodeList or assignStation:
                patient = {rowValue['tokenNumber']: patientCodeList}

                self.codeQueuelist[assignStation].put(patient) if assignStation else self.patientInqueue.update(patient)
            return

        data.apply(parseData, axis=1)
        return self.codeQueuelist, self.patientInqueue
