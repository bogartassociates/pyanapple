from elasticsearch import Elasticsearch
from datetime import datetime
from datetime import date
import re, json, time, boto, hashlib

#push an archived PineAP log to ElasticSearch over https with user/pw auth

fails = []

##### set these variables
#es_server = https://your.server
#creds = user:password
#logPath = '/home/data/archive/pineap_archive.log'
#es_index = 'smesh2'
#es_type = 'karma'
#####

def parseKarma(log):
    parsed = {}
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
              'May':'05','Jun':'06','Jul':'07','Aug':'08',
              'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    k_probe = '^([A-Z][a-z]{2}) +?(\d{1,2}) +?(\d{2}):(\d{2}):(\d{2}) +?(Probe Request from) +?([0-9a-f:]{17}) +?for SSID \'([^\']+)\''
    m = re.match(k_probe, log)
    k_association = '^([A-Z][a-z]{2}) +?(\d{1,2}) +?(\d{2}):(\d{2}):(\d{2}) +?([0-9a-f:]{17}) +?(trying to associate with) \'([^\']+)\''
    n = re.match(k_association, log)
    heartbeat_signature = '^([^\"]+)\", +\"as_of\": +\"(\d{8})_(\d{6})\"}'
    h = re.match(heartbeat_signature, log)
    if m:
        parsed['log_type'] = 'pineap'
        parsed['dtoi'] = str(date.today().year) + months[m.group(1)] + m.group(2).zfill(2) + m.group(3) + m.group(4) + m.group(5)
        parsed['producer'] = '01c6191c-1e5d-4107-a7bc-ad74f53a51ea'
        parsed['subject'] = m.group(7).replace(':','')
        parsed['subject_class'] = 'macAddress'
        parsed['verb'] = 'probe'
        parsed['object'] = m.group(8)
        parsed['object_class'] = 'SSID'
        parsed['hour_of_day'] = m.group(3)
    if n:
        parsed['log_type'] = 'pineap'
        parsed['dtoi'] = str(date.today().year) + months[n.group(1)] + n.group(2).zfill(2) + n.group(3) + n.group(4) + n.group(5)
        parsed['producer'] = '01c6191c-1e5d-4107-a7bc-ad74f53a51ea'
        parsed['subject'] = n.group(6).replace(':','')
        parsed['subject_class'] = 'macAddress'
        parsed['verb'] = 'association request'
        parsed['object'] = n.group(8)
        parsed['object_class'] = 'SSID'
        parsed['hour_of_day'] = n.group(3)
    if h:
        parsed['log_type'] = 'heartbeat'
        parsed['dtoi'] = str(h.group(1) + h.group(2))
        parsed['producer'] = h.group(1)
        parsed['subject'] = h.group(1)
        parsed['subject_class'] = 'system_component'
        parsed['verb'] = 'heartbeat'
    else:
        pass
    return parsed

es = Elasticsearch([es_server], port=9243, http_auth=creds)
with open(logPath, 'r', encoding='utf-8') as archive:
    for line in archive:
        doc = parseKarma(line)
        doc['dtoi'] = datetime.strptime(doc['dtoi'], '%Y%m%d%H%M%S')
        uniquify = hashlib.sha1(line.encode('utf-8')).hexdigest()
        res = es.index(index=es_index, doc_type=es_type, id=uniquify, body=doc)
        if res['created'] == False:
            fails.append(line)
        else:
            print(res['created'])