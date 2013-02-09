'''
Created on Feb 2, 2013

@author: kzaky
'''
import threading, re, Queue, time

class Peers(threading.Thread):

    def __init__(self, delete_queue):
        super(Peers, self).__init__()
        self.delete_queue = delete_queue
        self.stoprequest = threading.Event()

    def run(self):
        MyName = self.getName()
        stop = 0
        while (stop == 0):
            if not self.delete_queue.empty():
                DeletePeer = self.delete_queue.get()
                if (DeletePeer != MyName):
                    self.delete_queue.put(DeletePeer)
                else:
                    stop = 1    
            # here peer works on other stuff...

# print currently active peers (i.e., threads)
# 'MainThread' always included, but we do not show/count it
def PrintInfoCurrentPeers():
    peer_count = threading.active_count()-1
    print "Currently %d peers: " % peer_count
    for p in threading.enumerate():
        name = p.getName()
        if (name != 'MainThread'):
            print 'Peer:', name

# data structure containing peers to delete
delete_queue = Queue.Queue()

while 1:
    execute_command = 1
    PrintInfoCurrentPeers()
    command = raw_input("Enter command: ")
    words = command.split()

    if (len(words) == 0):
        execute_command = 0

    elif (execute_command == 1 and words[0] == "addp"):
        execute_command = 0
        p = Peers(delete_queue)
        p.setName(words[1])
        p.start()

    elif (execute_command == 1 and words[0] == "delp"):
        execute_command = 0
        delete_queue.put(words[1])

    elif (execute_command == 1 and words[0] == "delallp"):
        execute_command = 0
        for p in threading.enumerate():
            delete_queue.put(p.getName())

    elif (execute_command == 1):
        print "unknown command"