import paramiko

class Node:

    def __init__(self, ip, user, password, name):
        self.details = {}
        self.details['ip'] = ip
        self.details['user'] = user
        self.details['password'] = password
        self.details['name'] = name

    def connect(self):
        # on success, connection=active, else connection=failed
        ssh = paramike.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.details['ip'],
                    username=self.details['user'],
                    password=self.details['password'])
        self.ssh = ssh
        self.sftp = ssh.open_sftp()
        self.details['connection'] = 'Active'

    def disconnect(self):
        #on success, connection=inactive, else connection=failed
        self.sftp.close()
        self.ssh.close()
        self.details['connection'] = 'Inactive'
        pass

    def destruct(self, key):
        if key == '__DESTRUCT__':
            #blow up the node
            #rm /data
            #dd if=/dev/urandom of=/dev/sda bs=1000k
            self.details['destruct'] = 'Signal Sent'
            pass
        else:
            #reject
            self.details['destruct'] = 'Refused'
            pass