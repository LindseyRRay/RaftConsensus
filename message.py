#Message Class
from enum import Enum 

class Msg_Type(Enum):
    AppendEntries = 1
    AppendEntriesResponse = 2
    RequestVote = 3
    RequestVoteResponse = 4
    ClientRequest = 5
    ClientRequestResponse = 6
    FindLeader = 7
    FindLeaderResponse = 8

class Message:
	
	def __init__(self, sender, recipient, term=sender.current_term):
		self.senderID = sender.ID
		self.recipient = recipient
		self.term = term
	
				
class AppendEntries(Message):

	def __init__(self, sender, recipient, data):
		Message.__init__(self, sender, recipient)
		#sender will always be the leader
		self.leaderID = sender.ID
		self.prevLogIndex = sender.prevLogIndex
		try:
			self.prevLogTerm = sender.prevLogTerm
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

class RequestVote(Message):

	def __init__(self, sender, recipient, lastLogTerm, lastLogIndex):
		Message.__init__(self, sender, recipient)
		#index of last log entry
		#term of candidate's last log entry
		self.lastLogTerm = lastLogTerm 
		self.lastLogIndex = lastLogIndex
		self.type = Msg_Type.RequestVote


class RequestVoteResponse(Message):

	def __init__(self, sender, recipient, vote_granted):
		Message.__init__(self, sender, recipient)
		self.term = sender.current_term
		self.type = Msg_Type.RequestVoteResponse
		#reply false if msg term < current term
		#if have not voted for anyone, and candidates log is at least asup to date
		#then grant vote
		self.vote_granted = vote_granted

class ClientRequest:

	def __init__(self, recipient, command):
		self.recipient = recipient
		self.command = command
		self.type = Msg_Type.ClientRequest

class ClientRequestResponse:

	def __init__(self, sender, data):
		self.senderID = sender.ID
		self.commitIndex = data
		self.type = Msg_Type.ClientRequestResponse

class FindLeader:

	def __init__(self, recipient):
		self.recipient = recipient
		self.type = Msg_Type.FindLeader

class FindLeaderResponse:

	def __init__(self, sender, data):
		self.senderID = sender.ID
		self.term = sender.current_term
		self.data = data
		self.type = Msg_Type.FindLeaderResponse



			



