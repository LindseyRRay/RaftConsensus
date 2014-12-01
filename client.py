#Write client class
#client class responsible for sending log entries to leader
#client talks to random server, server sends back leader id once confirmed
#client then sends commands with terms

#implement match index checking for leaders
import threading
import time
from random import randint
from message import ClientRequest, FindLeader, FindLeaderResponse, ClientRequestResponse

class Client(threading.Thread):
    
    def __init__ (self, raft_instance):
        threading.Thread.__init__(self)
        self.raft_instance = raft_instance
        self.commands = list()
        self.commitIndex = 0
        self.message_queue = list()
        self.rlock = threading.RLock()
        self.currentLeader = None
        self.leaderIndex = 0
        self.lastCommand = None
        self.commandTimeOut = self.generate_election_time()
        self.daemon = True
    
    def generate_election_time(self):
        return randint(300,600)/1000


    def find_leader(self):
        #send message to each server in list
        with self.rlock:
            for server in self.raft_instance.server_nums:
                self.raft_instance.server_dict[server].queue_messages.append(FindLeader(server))
    
    def process_request_response(self, msg):
        #update commit index when leader communicates command has been committed to state machine
        #if receive a failing request response, initiate new find leader
        if not msg.data:
            self.find_leader()
        else:
            with self.rlock:
                self.commitIndex = max(self.commitIndex, msg.commitIndex)


    def process_leader_response(self, msg):
        if msg.data != None:
            self.currentLeader = msg.sender
            self.leaderIndex += 1
        else:
            #if no declared leader, sleep thread and then initiate new search
            time.sleep(5)
            self.find_leader()

    def process_messages(self):
        with self.rlock:
            for msg in self.message_queue:
                if msg.type == Msg_Type.FindLeaderResponse:
                    self.process_leader_response(msg)
                elif msg.type == Msg_Type.ClientRequestResponse:
                    self.process_request_response(msg)
                #pop off message from queue
                self.message_queue.pop()


    def send_command(self, command):
        with self.rlock:
            self.lastCommand = time.time()
            client_req = ClientRequest(self.currentLeader, command)
            for serv in self.raft_instance.server_dict.keys():
                self.raft_instance.server_dict[serv].queue_messages.append(client_req)
            self.commands.append(command)
            time.sleep(0)
  

    def command_timer(self):
        current = time.time()
        command = randint(-100,100)
        with self.rlock:
            try:
                print(self.commandTimeOut)
                if current > self.lastCommand + self.commandTimeOut:
                    print("Sending command")
                    self.send_command(command)
                else:
                    time.sleep(0)
            except:
                #first time
                self.send_command(command)


    def run(self):
      
        while True:
            self.command_timer()







