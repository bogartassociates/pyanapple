import paramiko


class Node:

    def __init__(self, ip, user, password, name):
        self.details = {}
        self.details['ip'] = str(ip)
        self.details['user'] = str(user)
        self.details['password'] = str(password)
        self.details['name'] = str(name)
        self.ssh = paramiko.SSHClient()
        self.sftp = None

    def connect(self):
        # on success, connection=active, else connection=failed
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
                        self.details['ip'],
                        username=self.details['user'],
                        password=self.details['password']
                        )

        self.sftp = self.ssh.open_sftp()
        self.details['connection'] = 'Active'

    def disconnect(self):
        # on success, connection=inactive, else connection=failed
        self.sftp.close()
        self.ssh.close()
        self.details['connection'] = 'Inactive'
        pass

    def destruct(self, key):
        if key == '__DESTRUCT__':
            # blow up the node
            # rm /data
            # dd if=/dev/urandom of=/dev/sda bs=1000k
            self.details['destruct'] = 'Signal Sent'
            pass
        else:
            # reject
            self.details['destruct'] = 'Refused'
            pass
