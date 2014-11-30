#Message Class
from enum import Enum 

class Msg_Type(Enum):
    AppendEntries = 1
    AppendEntriesResponse = 2
    RequestVote = 3
    RequestVoteResponse = 4

class Message:
	
	def __init__(self, sender, recipients):
		self.senderID = sender.ID
		self.SERVER_IDS = sender.SERVER_IDS
		self.recipients = self.parse_recipients(recipients)
		self.term = sender.current_term
		

	def parse_recipients(self, recipients):
		#if recipients are all servers
		if recipients[0] == 'a':
			list_recipients = [str(server) for server in self.SERVER_IDS if server != self.senderID]
			return list_recipients
		else:
			return recipients
		
				
class AppendEntries(Message):

	def __init__(self, sender, recipients, data):
		Message.__init__(self, sender, recipients)
		#sender will always be the leader
		self.leaderID = sender.ID
		self.prevLogIndex = sender.log.prevLogIndex
		try:
			self.prevLogTerm = sender.log.log[self.prevLogIndex].term 
		except:
			self.prevLogTerm = 0
		self.entries = data
		self.leaderCommit = sender.log.CommitIndex
		self.type = Msg_Type.AppendEntries

class AppendEntriesResponse(Message):

	def __init__(self, sender, leaderID, success):
		Message.__init__(self, sender, leaderID)
		self.term = sender.current_term
		self.success = success
		self.success_indices = list()
		self.type = Msg_Type.AppendEntriesResponse

	#def consistency_check(self):
		#reply false if term < current Term
	#	if self.current_term > self.term:
			#return False
		#reply false if log deoesn't contain an entry at prev log index who matches
	#	if sender.log.log[AppendEntries.prevLogIndex].term != AppendEntries.prevLogTerm:
		#	return False
		#if existing entry conflicts with new one (same index, but diff terms, 
			#delete existing entry and all that follow)
		#append entrues not in log
		#if leader commit > commit index, then commitindex = min(leadercommit, index of last new entry)

class RequestVote(Message):

	def __init__(self, sender, recipients):
		Message.__init__(self, sender, recipients)
		#index of last log entry
		self.lastLogIndex = sender.log.lastLogIndex
		#term of candidate's last log entry
		self.type = Msg_Type.RequestVote
		try:
			self.lastLogTerm = sender.log.log[self.lastLogIndex].term
		except:
			self.lastLogTerm = 0

class RequestVoteResponse(Message):

	def __init__(self, sender, recipients, vote_granted):
		Message.__init__(self, sender, recipients)
		self.term = sender.current_term
		self.type = Msg_Type.RequestVoteResponse
		#reply false if msg term < current term
		#if have not voted for anyone, and candidates log is at least asup to date
		#then grant vote
		self.vote_granted = vote_granted
			



