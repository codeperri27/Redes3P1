from calls import DB_FILENAME, TEMPLATE_FILE

import snmpQuery
import rrdtool
import pdfkit
import jinja2
import os

class SnmpReportGenerator:

    def __init__(self, agentInfo):
        self.resourceFolder = agentInfo.getIdentifier()
        self.agentInfo = agentInfo
        self.loadTemplate()

    def loadTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath = './')
        templateEnv = jinja2.Environment(loader = templateLoader)
        self.template = templateEnv.get_template(TEMPLATE_FILE)
    
    # This has to be cleaner.
    def renderGraphs(self, startTime, endTime):
        rrdtool.graph(self.resourceFolder + '/ifInUcastPkts.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('outnucast',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ifInUcastPkts',
                        'AVERAGE'
                    ),
                'AREA:outnucast#0000FF:Paquetes unicast que ha recibido una interfaz'
            )
        rrdtool.graph(self.resourceFolder + '/ipInReceives.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('ipout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ipInReceives',
                        'AVERAGE'
                    ),
                'AREA:ipout#00FF00:Solicitudes IP incluyendo los que tienen errores'
            )
        rrdtool.graph(self.resourceFolder + '/icmpOutMsgs.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=ICMP Msgs/s',
                'DEF:{0}={1}:{2}:{3}'.format('icmp',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'icmpOutMsgs',
                        'AVERAGE'
                    ),
                'AREA:icmp#FF0000:Mensajes ICMP que ha enviado el agente'
            )
        rrdtool.graph(self.resourceFolder + '/tcpOutSegs.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=TCP Retrans/s',
                'DEF:{0}={1}:{2}:{3}'.format('tcpret',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'tcpOutSegs',
                        'AVERAGE'
                    ),
                'AREA:tcpret#000000:Segmentos TCP  enviados, incluyendo los de las conexiones actual pero excluyendo los que contienen solamente octetos transmitidos.'
            )
        rrdtool.graph(self.resourceFolder + '/udpInDatagrams.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=UDP Datagrams/s',
                'DEF:{0}={1}:{2}:{3}'.format('udpout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'udpInDatagrams',
                        'AVERAGE'
                    ),
                'AREA:udpout#777777:Datagramas enviados.'
            )

    def getAgentSysInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.1'
            )
    
    def renderHTML(self):
        sysInfo = self.getAgentSysInfo()

        # This is just because I'm rushing
        sysDescr = sysInfo['1.3.6.1.2.1.1.1.0'].lower()
        logo = ''
        if 'windows' in sysDescr:
            logo = 'windows.png'
        elif 'linux' in sysDescr:
            logo = 'linux.png'

        self.renderedHTML = self.template.render(
                agentOSLogo = os.path.abspath(logo),
                agentSysName = sysInfo['1.3.6.1.2.1.1.5.0'],
                agentSysDescr = sysInfo['1.3.6.1.2.1.1.1.0'],
                agentSysUpTime = sysInfo['1.3.6.1.2.1.1.3.0'],
                agentSysContact = sysInfo['1.3.6.1.2.1.1.4.0'],
                agentSysLocation = sysInfo['1.3.6.1.2.1.1.6.0'],
                ifGraphFile = os.path.abspath(
                    self.resourceFolder + '/ifInUcastPkts.png'),
                ipGraphFile = os.path.abspath(
                    self.resourceFolder + '/ipInReceives.png'),
                icmpGraphFile = os.path.abspath(
                    self.resourceFolder + '/icmpOutMsgs.png'),
                tcpGraphFile = os.path.abspath(
                    self.resourceFolder + '/tcpOutSegs.png'),
                udpGraphFile = os.path.abspath(
                    self.resourceFolder + '/udpInDatagrams.png')
            )

    def makeReport(self, fileName, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf')
