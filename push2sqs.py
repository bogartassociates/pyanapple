#push to sqs. use boto config to set api keys

import os, time, random, boto, shutil, json
from boto import sqs
from boto.sqs.message import Message

conn = sqs.connect_to_region('us-east-1')
q = conn.create_queue('chairOne')

while 1 == 1:
    time.sleep(1)
    to_process = []
    for newlog in os.listdir('/home/data/newlogs'):
        to_process.append('/home/data/newlogs/' + newlog)

    for newlog in to_process:
        with open(newlog, 'r') as thefile:
            lines = thefile.readlines()
            for line in lines:
                print(line[:-1])
                m = Message()
                m.set_body(json.dumps({"pineap":line}))
                q.write(m)
        newloc = newlog.replace('newlogs', 'oldlogs')
        shutil.move(newlog, newloc)
        to_process.remove(newlog)
