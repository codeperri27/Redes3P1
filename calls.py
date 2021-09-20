#SNMP Version Constants according to the API.

SNMP_V2C = 1
SNMP_V1 = 0

#Monitor Constants.

MONITOR_FREQ = 10

#Nodes to be monitored.

SIMPLE_NODES = sorted(
        [
            'udpInDatagrams',
            'tcpOutSegs',
            'ipInReceives',
            'icmpOutMsgs'
        ]
    )

COMPLEX_NODES = sorted(
        [
            'ifInUcastPkts'
        ]
    )

NAME_TO_OID = {

        'ifInUcastPkts'     : '1.3.6.1.2.1.5.13.0', #unicast
        'icmpOutMsgs'       : '1.3.6.1.2.1.7.13.0', #icmpInMsgs
        'udpInDatagrams'    : '1.3.6.1.2.1.7.1.0', #datagramas 
        'tcpOutSegs'        : '1.3.6.1.2.1.6.11.0', #segmentos enviados
        'ipInReceives'      : '1.3.6.1.2.1.4.3.0' # total de datagramas incluyedo erorres
    }

COMPLEX_OIDS = [NAME_TO_OID[name] for name in COMPLEX_NODES]
SIMPLE_OIDS = [NAME_TO_OID[name] for name in SIMPLE_NODES]

OID_TO_NAME = dict()
for x in range(0, len(COMPLEX_OIDS)):
    OID_TO_NAME[COMPLEX_OIDS[x]] = COMPLEX_NODES[x]
for x in range(0, len(SIMPLE_OIDS)):
    OID_TO_NAME[SIMPLE_OIDS[x]] = SIMPLE_NODES[x]

#RRDTool Constants

DB_FILENAME = 'snmp.rrd'
RRD_COUNTER = 'COUNTER'
RRD_THRESHOLD = '60'
RRD_UNKNOWN = 'U'
RRD_STEP = '20'
RRD_NOW = 'N'

NAME_TO_RRDTYPE = {
        'ifInUcastPkts'     : RRD_COUNTER,
        'udpInDatagrams'    : RRD_COUNTER,
        'tcpOutSegs'        : RRD_COUNTER, 
        'ipInReceives'      : RRD_COUNTER,
        'icmpOutMsgs'       : RRD_COUNTER
    }

#Report Generator Constants.

TEMPLATE_FILE = 'reportTemplate.html'

