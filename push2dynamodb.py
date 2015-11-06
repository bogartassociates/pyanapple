#use boto config to set api keys

from boto import sqs, dynamodb2
from boto.dynamodb2.table import Table
from datetime import date
import re, json, time, boto

def parseKarma(log):
    parsed = {}
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
              'May':'05','Jun':'06','Jul':'07','Aug':'08',
              'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    k_probe = '^{\"(pineap)\": +?\"([A-Z][a-z]{2}) +?(\d{1,2}) +?(\d{2}):(\d{2}):(\d{2}) +?(Probe Request from) +?([0-9a-f:]{17}) +?for
 SSID \'([^\']+)\''
    m = re.match(k_probe, log)
    k_association = '^{\"(pineap)\": +?\"([A-Z][a-z]{2}) +?(\d{1,2}) +?(\d{2}):(\d{2}):(\d{2}) +?([0-9a-f:]{17}) +?(trying to associate
 with) \'([^\']+)\''
    n = re.match(k_association, log)
    heartbeat_signature = '^{\"heartbeat\": +\"([^\"]+)\", +\"as_of\": +\"(\d{8})_(\d{6})\"}'
    h = re.match(heartbeat_signature, log)
    if m:
        parsed['log_type'] = m.group(1)
        parsed['dtoi'] = str(date.today().year) + months[m.group(2)] + m.group(3).zfill(2) + m.group(4) + m.group(5) + m.group(6)
        parsed['producer'] = '01c6191c-1e5d-4107-a7bc-ad74f53a51ea'
        parsed['subject'] = m.group(8).replace(':','')
        parsed['subject_class'] = 'macAddress'
        parsed['verb'] = 'probe'
        parsed['object'] = m.group(9)
        parsed['object_class'] = 'SSID'
    if n:
        parsed['log_type'] = n.group(1)
        parsed['dtoi'] = str(date.today().year) + months[n.group(2)] + n.group(3).zfill(2) + n.group(4) + n.group(5) + n.group(6)
        parsed['producer'] = '01c6191c-1e5d-4107-a7bc-ad74f53a51ea'
        parsed['subject'] = n.group(7).replace(':','')
        parsed['subject_class'] = 'macAddress'
        parsed['verb'] = 'association request'
        parsed['object'] = n.group(9)
        parsed['object_class'] = 'SSID'
    if h:
        parsed['log_type'] = 'heartbeat'
        parsed['dtoi'] = str(h.group(2) + h.group(3))
        parsed['producer'] = h.group(1)
        parsed['subject'] = h.group(1)
        parsed['subject_class'] = 'system_component'
        parsed['verb'] = 'heartbeat'
    else:
        pass
    return parsed

conn = sqs.connect_to_region("us-east-1")
q = conn.create_queue('chairOne')
wingBack = Table('wingBack', connection=dynamodb2.connect_to_region('us-east-1'))

while 1 == 1:
    time.sleep(1)
    try:
        if q.count() > 0:
            m = q.get_messages(visibility_timeout=6000)[0]
            print(str(q.count()) + ' items in chairOne queue at ' + time.strftime('%Y%m%d_%H%M%S'))
            print(m.get_body())
            record = parseKarma(m.get_body())
            if len(record) > 0:
                try:
                    if wingBack.put_item(record) == True:
                        q.delete_message(m)
                    else:
                        print('PUTing failed!')
                except boto.dynamodb2.exceptions.ConditionalCheckFailedException:
                    q.delete_message(m)
            elif re.match('.*DTF.*S.*', m.get_body()):
                q.delete_message(m)
            else:
                print('__________need a case for:')
                print(m.get_body())
        else:
            print('no messages')
            time.sleep(2)
    except:
        time.sleep(2)
	print('no messages')