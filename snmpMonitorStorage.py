from pip._internal.utils import logging

from utilityFunctions import BuildDataSourceString

import calls
import rrdtool
import os

class SnmpMonitorStorage:

    def __init__(self, snmpAgentInfo):
        self.makeStorageFile(snmpAgentInfo)
        self.createDatabase()

    def makeStorageFile(self, snmpAgentInfo):
        self.path = snmpAgentInfo.getIdentifier()

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + calls.DB_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        if os.path.isfile(self.fileName):
            return

        dataSources = []
        for name in calls.SIMPLE_NODES:
            dataSources.append(
                    BuildDataSourceString(name,
                                          calls.NAME_TO_RRDTYPE[name])
                )
        for name in calls.COMPLEX_NODES:
            dataSources.append(
                    BuildDataSourceString(name,
                                          calls.NAME_TO_RRDTYPE[name])
                )
        errorCode = rrdtool.create(self.fileName,
                '--start', calls.RRD_NOW,
                '--step', calls.RRD_STEP,
                                   *dataSources,
                'RRA:AVERAGE:0.5:1:270',
                                   )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise
    
    def updateDatabase(self, updateValues):
        updateString = calls.RRD_NOW
        for name in calls.SIMPLE_NODES:
            updateString += ':'
            if name in updateValues:
                updateString += str(updateValues[name])
            else:
                updateString += calls.RRD_UNKNOWN
        for name in calls.COMPLEX_NODES:
            updateString += ':'
            if name in updateValues:
                updateString += str(updateValues[name])
            else:
                updateString += calls.RRD_UNKNOWN
        rrdtool.update(self.fileName, updateString)

