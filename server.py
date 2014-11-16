from enum import Enum 
from random import randint
import threading
import time
from queue import Queue 

from raft import SERVER_IDS

from message import Message 

HEARTBEAT_TIMEOUT = 1

class State(Enum):
    follower = 1
    candidate = 2
    leader = 3


class Server(threading.Thread):
    def __init__(self, server_id):
        #persistent attributes
        threading.Thread.__init__(self)
        self.ID = server_id
        self.state = State.candidate
        self.set_daemon = True

        self.current_term = 0
        self.voted_for = None
        self.log = list()
        self.queue_messages = QUEUE()
        self.last_update = time.time()
        self.election_start = None
        self.election_time = self.generate_election_time()
        self.peers = [p for p in SERVER_IDS if p != self.ID]
        self.total_votes = 0


        #volatile attributes
        self.commit_index = None
        self.last_applied = 0

        #Leader attributes
        self.next_index = 0 
        self.match_index = 0

    def generate_election_time(self):
        return random.randint(150,300)/1000

    def update_timers(self):
        now = time.time()
        if self.state == State.candidate:
            elapsed = now - self.election_start
        #check for a dead leader, call election if leader dead
        if now - self.last_update > HEARTBEAT_TIMEOUT and self.state == State.follower:
            self.call_election()
        #Election timer still not elapsed, check for messages- no action
        elif self.state == State.candidate and elapsed < self.election_time:
            #check for messages
        #Election timer ran out, not converted to another state, request votes
        elif self.state == State.candidate and elapsed > self.election_time:
            self.call_election()
        #if follower check to make
        elif self.state = State.Leader:
            self.send_heartbeat()


    def call_election(self):
        print("Calling Election %s" %self.ID) 
        #create random timer, when it times out, send out Request for Vote Messages
        #possibly clear message queue
        self.election_time = self.generate_election_time()
        self.election_start = time.time()
        #self.queue_messages = list()
        self.state = State.candidate
        self.voted_for = None
        self.current_term += 1
        #reset message queue
        self.queue_messages = QUEUE()
        self.request_votes()
        #self.state_manager.next_step()

    def request_votes(self):
        print("Asking for votes %s" %self.ID)
        self.send_message(recip = 'all_servers', type = 'RFV')


    def send_vote(self):  
        print("sending vote %s" %self.ID)  
        recip = 'all_servers', msg_type='HEARTBEAT'
        self.send_message(recip = self.voted_for, msg_type = 'RFV_YES"') 


    def process_heartbeat(self, msg):
        print("processing heartbeat %s" %self.ID)
        #if get heartbeat, update time of last update
        if self.state == State.follower and msg.term >= self.current_term:
            self.last_update = time.time()
            #update term of the member if less than existing term
            self.current_term = msg.term
        #if current state is candidate, and term >= current, update to follower
        if self.state in [State.candidate, State.Leader] and msg.term >= self.current_term:
            self.last_update = time.time()
            self.current_term = msg.term
            self.state = State.follower
            self.voted_for = None
 

    def process_vote_request(self, msg):
        print("processing vote request %s" %self.ID)
        if self.state == state.candidate and self.voted_for == None and msg.current_term >= self.current_term:
            self.voted_for = msg.sender
            self.current_term = msg.term
            #DO people inmediatly convert to follower
            self.state = State.follower
            self.send_vote()
        else:
            #remove message from message queue
            return

    def process_vote_response(self, msg): 
        #Calculate vote responses and add to tally to
        #calculate majority
        if self.state == state.candidate and msg.term == self.current_term:
            self.total_votes += 1

        if self.total_votes >= len(self.peers)/2:
            self.state = state.leader
            self.become_leader()

    def become_leader(self):
        self.send_heartbeat()
        self.queue_messages = QUEUE()
        self.voted_for = None

    def send_heartbeat(self):
        print("Sending heartbeat %s" %self.ID)
        self.send_message(recip = 'all_servers', msg_type='HEARTBEAT')

    def send_message(self, recip, msg_type):
        #Create a new message and add arguments
        print("Sending message %s" %self.ID)
        #Add message to universal queue
        msg = Message(sender = self.ID, recipients = recip, msg_type = msg_type, term = self.current_term)

        #GLOBAL QUEUE ADD INFO
        GLOBAL_QUEUE.APPEND(msg)


    def next_step(self):
        print("Sending heartbeat %s" %self.ID)

if __name__ == '__main__':
    test_server = Server()


    def check_vote_queue(self):

        for i, msg in self.queue_messages:
            while self.state == State.candidate and self.voted_for == None:
                if msg.type == "RFV" and msg.term >= self.current_term:
                    self.voted_for = self.msg.server_id
                    self.state = State.follower
                    self.current_term = msg.term
                    self.queue_messages.pop(i) 
                    self.state_manager.next_step()





