from .NodeManager import *
from .Node import *
from .test import *





"""
def moveLogs():
    for incoming in os.walk('/home/data/incoming'):
        for logfile in incoming[2]:
            newname = '/home/data/newlogs/' + time.strftime('%Y%m%d_%H%M%S') + logfile
            oldname = incoming[0] + '/' + logfile
            shutil.move(oldname, newname)
            time.sleep(1)





def move2newlogs():
    for incoming in os.walk('/home/data/incoming'):
        for logfile in incoming[2]:
            newname = '/home/data/newlogs/' + time.strftime('%Y%m%d_%H%M%S') + logfile
            oldname = incoming[0] + '/' + logfile
            shutil.move(oldname, newname)
            time.sleep(1)

while 1 == 1:
    time.sleep(1)
    try:
        ssh = paramiko.SSHClient()
        #temporary - add host to ~/.ssh/known_hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_ip,username=ssh_user,password=ssh_pw)
        ftp = ssh.open_sftp()
        ftp.get('/sd/logs/pineap.log', '/home/data/incoming/pineap.log')
        ftp.close()
        ssh.exec_command('rm /sd/logs/pineap.log')
        ssh.close()
        move2newlogs()
    except:
        pass
"""