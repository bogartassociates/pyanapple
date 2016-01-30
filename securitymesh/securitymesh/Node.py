class Node:

    def __init__(self, ip, user, password, name):
        self.details = {}
        self.details['ip'] = ip
        self.details['user'] = user
        self.details['password'] = password
        self.details['name'] = name

    def connect(self):
        #open ssh connection
        # on success, connection=active, else connection=failed
        self.details['connection'] = 'Active'
        pass

    def disconnect(self):
        #close ssh connection
        #on success, connection=inactive, else connection=failed
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