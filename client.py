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
        self.leaderTracking= list()
        self.lastCommandTime = None
        self.lastLeaderTime = None
        self.commandTimeOut = self.generate_election_time()
        self.daemon = True
    

    def find_leader(self):
        #send message to each server in list
        logging.debug("Finding Leader")
        with self.rlock:
            for server in self.raft_instance.server_nums:
                find_lead_message = FindLeader(server)
                self.raft_instance.message_queue.append(find_lead_message)
          
    def process_request_response(self, msg):
        #update commit index when leader communicates command has been committed to state machine
        #if receive a failing request response, initiate new find leader
        logging.debug("Processing Req Response ")
        if not msg.data or self.currentLeader != msg.senderID or msg.term != self.leaderTracking[-1][1]:
            time.sleep(2)
            self.find_leader()
        else:
            with self.rlock:
                self.commitIndex = max(self.commitIndex, msg.commitIndex)


    def process_leader_response(self, msg):
        current = time.time()
        if msg.data != None:
            logging.debug("Found leader %s"%self.currentLeader)
            self.currentLeader = msg.sender
            self.leaderTracking.append((msg.sender, msg.term))
            #reset last leader time
            self.lastLeaderTime = time.time()
            #set leader attempts back to 0
            self.leaderTries = 0
        else:
            #if no declared leader, sleep thread and wait for more messages
            self.leaderTries +=1 
            if self.leaderTries == self.raft_instance.number_servers or self.lastLeaderTime + 60 > current:
                self.find_leader()
            #if haven't received replies from all servers, call election
            time.sleep(5)


    def get_messages(self):
        #get messages from the message queue
        while self.message_queue:
            with self.rlock:
                yield self.message_queue.pop()

    def process_messages(self):
        with self.rlock:
            for msg in self.get_messages():
                if msg.type == Msg_Type.FindLeaderResponse:
                    self.process_leader_response(msg)
                elif msg.type == Msg_Type.ClientRequestResponse:
                    self.process_request_response(msg)
      

    def send_command(self, command):
        #send command to leader to add new entry to server log
        with self.rlock:
            self.lastCommandTime = time.time()
            client_req = ClientRequest(self.currentLeader, command)
            self.raft_instance.message_queue.append(client_req)
            time.sleep(0)
  

    def command_timer(self):
        #check command timeout and then try to send a commnd
        #if get back as response that with False
        current = time.time()
        command = randint(-100,100)
        if self.currentLeader:
            with self.rlock:
                try:
                    if current > self.lastCommandTime + self.commandTimeOut:
                        print("Sending command")
                        self.send_command(command)
                    time.sleep(0)
                except:
                    #first time
                    self.send_command(command)
        self.find_leader()


    def run(self):
      
        while True:
            self.command_timer()







