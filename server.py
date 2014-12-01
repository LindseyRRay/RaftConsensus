from enum import Enum 
from random import randint
import threading
import time
from queue import Queue 
import pudb
import pdb
import logging


#import logging and debugging 
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

#Need to create client and tie match index and next index to each server
from message import Message, AppendEntries, AppendEntriesResponse, RequestVote, RequestVoteResponse, FindLeader, FindLeaderResponse, ClientRequest, ClientRequestResponse, Msg_Type
from log import Log, LogEntry

HEARTBEAT_TIMEOUT = 1



class State(Enum):
    follower = 1
    candidate = 2
    leader = 3


class Server(threading.Thread):
    def __init__(self, server_id, Raft_instance):
        #persistent attributes
        threading.Thread.__init__(self)
        self.ID = str(server_id)
        self.state = State.candidate
        self.daemon = True
        self.rlock = Raft_instance.rlock
        self.SERVER_IDS = Raft_instance.server_nums
        self.Raft_instance = Raft_instance

        self.current_term = 0
        self.voted_for = None

        #self.queue_messages = Queue()
        self.queue_messages= list()
        self.last_update = time.time()
        self.election_start = None
        self.election_time = self.generate_election_time()
        self.peers = [p for p in self.SERVER_IDS if p != self.ID]
        self.total_votes = 0

        #volatile attributes
 
        self.last_applied = 0
        self.currentLeader = None

        #log attributes
        self.log = Log()

        #Leader attributes


#generate election timeout interval
    def generate_election_time(self):
        #return randint(150,300)/1000
        return randint(15,300)/1000

    def update_timers(self):
        #need to fix elapsed METHOD, throwing an error
        now = time.time()
        if self.state == State.candidate:
            try:
                elapsed = now - self.election_start
                #check for a dead leader, call election if leader dead
                if now - self.last_update > HEARTBEAT_TIMEOUT and self.state == State.follower:
                    self.call_election()
                #Election timer still not elapsed, check for messages- no action
                elif self.state == State.candidate and elapsed < self.election_time:
                    return
                    #check for messages
                #Election timer ran out, not converted to another state, request votes
                elif self.state == State.candidate and elapsed > self.election_time:
                    time.sleep(5)
                    self.call_election()
                #if follower check to make
                elif self.state == State.Leader:
                    self.send_heartbeat()

            #if election_start is still NONE, then this is first initialization
            except:
                self.call_election()
        if self.state == State.leader:
            self.send_heartbeat()


    def call_election(self):
        #logging.debug("Calling Election %s" %self.ID) 
        #create random timer, when it times out, send out Request for Vote Messages
        #possibly clear message queue
        #clear election queue
        #self.queue_messages = Queue()
        self.queue_messages = list()
        self.election_time = self.generate_election_time()
        self.election_start = time.time()
        
        self.currentLeader = None
        self.state = State.candidate
        self.voted_for = None
        self.current_term += 1

        self.send_requestvote()
        #self.state_manager.next_step()

    def send_requestvote(self):
        #logging.debug("Asking for votes %s" %self.ID)
        #send message to all servers asking for votes
        self.send_message(recip = 'all_servers', msg_type = Msg_Type.RequestVote)

#sending vote function
    def send_vote(self):  
        #logging.debug("sending vote: %s for: %s" %(str(self.ID), str(self.voted_for))) 
        with self.rlock:
            self.send_message(recip = [self.voted_for], msg_type = Msg_Type.RequestVoteResponse, data = True) 
    
    def send_heartbeat_response(self, success):
        self.send_message(recip =[self.currentLeader], msg_type = Msg_Type.AppendEntriesResponse, data = success)
#process a heartbeat message

    def process_heartbeat(self, msg):
        #logging.debug("processing heartbeat %s" %self.ID)
        #if get heartbeat, update time of last update
        if self.state == State.follower:
            if msg.term >= self.current_term:
                self.last_update = time.time()
            #update term of the member if less than existing term
                self.current_term = msg.term
                self.currentLeader = msg.leaderID
            elif msg.term < self.current_term:
                self.send_heartbeat_response(data=False)
            elif self.log.log[log.prevLogIndex].term != msg.prevLogTerm:
                self.send_heartbeat_response(data=False)
                #reply false if log doesn't contain an entry at prevLog Index whose term matches prevLogTerm
        if self.state == State.follower and len(msg.entries) > 0:
            self.compare_logs(msg)
            self.append_entries(msg)
#if leader commit > commit index, setc commit index = min(leaderCommit, index of last new entry)
            if msg.leaderCommit > self.log.commitIndex:
                self.log.commitIndex = min(msg.leaderCommit, log.prevLogIndex)

 
        #if current state is candidate, and term >= current, update to follower
        #this means the server is behind the other servers and needs to fast forward
        elif self.state in [State.candidate, State.leader] and msg.term > self.current_term:
            self.last_update = time.time()
            self.current_term = msg.term
            self.state = State.follower
            self.voted_for = None
        else :
            return 
        #add check to only send heartbeat if no one in the global queue
        #if you receive a heartbeat from yourself, then send out another one to global queue
        #elif self.state == State.leader and msg.term == self.current_term:
            #if len(self.Raft_instance.message_queue) ==0 or str(self.Raft_instance.message_queue[0].sender) == str(self.server_id):
                #pass
           # else:
              #  self.send_heartbeat()
    #append any new entries not in the log
    def append_entries(self, msg):
        for index, entry in msg.entries:
            if index > len(self.log.log)-1:
                self.log.log.append(entry)
        #update prevLogIndex
        self.log.prevLogIndex = len(self.log.log)-1

    def compare_logs(self, msg):
        #if an existing entry conflicts with a new one (same index but dif terms),
        # delete existing entry and all that follow
        for index, entry in msg.entries:
            if len(self.log.log)-1 < index:
                continue
            elif entry.term != self.log.log[index].term:
                self.log.log.remove(self.log.log[index])

    def check_commit_indices(self):
        for index, log in enumerate(self.l.logog.log):
            if log.success_count > len(self.peers)/2:
                self.log.commitIndex = index
        self.send_heartbeat()   
       
    def process_heartbeat_response(self, msg):
        if self.state == State.leader and msg.term ==self.current_term:
            #if append entry successful, add that to the log
            if msg.success:
                #increment count of servers with entry
                for index, term in msg.success_indices:
                    if self.log.log[index].term == term:
                        self.log.log[index].success_count += 1
                    else:
                        RuntimeError("This Should NOT happen")
                #if now a majority, then commit and increment commit index
                self.check_commit_indices()
        else:
            return


    def process_vote_request(self, msg):
        #print("processing vote request %s" %self.ID)
        if self.state == State.candidate and self.voted_for == None and msg.term >= self.current_term:
            self.voted_for = str(msg.senderID)
            self.current_term = msg.term
            self.send_vote()


    def process_vote_response(self, msg): 
        #Calculate vote responses and add to tally to
        #calculate majority
       # logging.debug("processing vote response %s" %self.ID)
        if self.state == State.candidate and msg.term == self.current_term :
            self.total_votes += 1
            logging.debug("total votes %s" %self.total_votes)
#become a leader if you receive a majority of your peers in votes
        if self.total_votes > len(self.peers)/2:
            self.state = State.leader
            self.current_term += 1
            self.become_leader()
#change state to leader
#send out heartbeat, clear your queue list
    def become_leader(self):
        #logging.debug("becoming leader %s" %self.ID)
        self.send_heartbeat()
        self.currentLeader = self.ID
        #self.queue_messages = Queue()
        self.queue_messages = list()
        self.voted_for = None
        # Reinitialize last indices
        self.next_index = dict() 
        self.match_index = dict()

    def reinitialize_match_indices(self):
        self.next_index = {p: self.log.lastLogIndex+1 for p in peers}
        self.match_index = {p: 0 for p in peers}

    def send_heartbeat(self, data =[]):
        #logging.debug("Sending heartbeat %s" %self.ID)
        #send heartbeat with new commit index, info associated from client
        self.send_message(recip = 'all_servers', msg_type=Msg_Type.AppendEntries, data = data)


    def send_message(self, recip, msg_type, data=[]):
        #Create a new message and add arguments
        #logging.debug("Sending message %s to %s" %(str(self.ID), str(recip)))
        #Add message to universal queue
        #pass server IDS to the current message
        if msg_type == Msg_Type.AppendEntries:
            msg = AppendEntries(self, recipients = recip, data = data)
        elif msg_type == Msg_Type.AppendEntriesResponse:
            msg = AppendEntriesResponse(self, self.currentLeader, data = data)
        elif msg_type == Msg_Type.RequestVote:
            msg = RequestVote(self, recipients = recip)
        elif msg_type == Msg_Type.RequestVoteResponse:
            msg = RequestVoteResponse(self, recip, vote_granted = data)
        elif msg_type == Msg_Type.FindLeaderResponse:
            msg = FindLeaderResponse(data)
        elif msg_type == Msg_Type.ClientRequestResponse:
            msg = ClientRequestResponse(self.ID, data)

        else:
            raise Exception("Unknown type of Message")

        #GLOBAL QUEUE ADD INFO
        with self.rlock:
            #adding message to Raft instance global queue
            #self.Raft_instance.message_queue.put(msg)
            self.Raft_instance.message_queue.append(msg)
            #logging.debug("Adding to GLOBAL queue from %s"%self.ID)
    #organizing function for reading messages

    def process_client_request(self, msg):
        #if you are leader you need to correctly process client request
        #if you are the leader, add command to your log
        if self.state == State.leader:
            with self.rlock:
                newEntry = LogEntry(self.current_term, msg.data)
                self.log.log.append(newEntry)
                self.log.increment_prevLogIndex()
                self.send_heartbeat(newEntry)
        else:
            #client doesn't know who leader is anymore, tell client to initiate search
            self.send_message("client", Msg_Type.ClientRequestResponse, False)
      
    
    def process_find_leader(self, msg):
        self.send_message("client", Msg_Type.FindLeaderResponse, self.currentLeader)
      

    def check_messages(self):
        #logging.debug("Checking Messages %s an len is %s" %(self.ID, len(self.queue_messages)))
        logging.debug("State %s" %self.state)
        if len(self.queue_messages) == 0 and self.state == State.leader:
            self.send_heartbeat()
        while len(self.queue_messages) > 0 :
            self.process_message(self.queue_messages.pop())

       # while not self.queue_messages.empty():
         #   self.process_message(self.queue_messages.get())
            
            #remove message if term is < current ter

    def process_message(self, msg):
        #remove old messages from queue
        #logging.debug("Processing messages %s" %self.ID)    
        # if msg.term < self.current_term:
        #    # print("No messages")
        #     return
        if msg.type == Msg_Type.FindLeader:
            self.process_find_leader(msg)

        elif msg.type == Msg_Type.ClientRequest:
            self.process_client_request(msg)

        elif msg.type == Msg_Type.AppendEntries:
            self.process_heartbeat(msg)

        elif msg.type == Msg_Type.AppendEntriesResponse:
            self.process_heartbeat_response(msg)

        elif msg.type == Msg_Type.RequestVote:
            self.process_vote_request(msg)

        elif msg.type == Msg_Type.RequestVoteResponse:
            self.process_vote_response(msg)

        else:
            print("Bad")
            print(msg.type)

    def run(self):
        #while self.Raft_instance.Run:
        while True:
            #logging.debug("thread updating timers")
            self.update_timers()
            #logging.debug("thread checking messages")
            self.check_messages()




if __name__ == '__main_u_':

    GLOBAL_QUEUE = Queue()
    rlock = threading.RLock()
    test_msg = Message('234', ['123', '234'], Msg_Type.AppendEntries, 1)
    test_server = Server('123', rlock)
    test_server.call_election()
    pdb.set_trace()







