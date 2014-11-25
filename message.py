#Message Class

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

	def __init__(self, sender, recipients):
		Message.__init__(self, sender, recipients)
		#sender will always be the leader
		self.leaderID = sender.ID
		self.prevLogIndex = sender.log.prevLogIndex
		self.prevLogTerm = sender.log[prevLogIndex].term 
		self.entries = sender.log.entries
		self.leaderCommit = sender.log.CommitIndex

class AppendEntriesResponse(Message):

	def __init__(self, sender, AppendEntries, success):
		Message.__init__(self, sender, AppendEntries.leaderID)
		self.term = sender.current_term
		self.success = self.consistency_check()

	def consistency_check(self):
		#reply false if term < current Term
		if self.current_term > AppendEntries.term:
			return False
		#reply false if log deoesn't contain an entry at prev log index who matches
		if sender.log[AppendEntries.prevLogIndex].term != AppendEntries.prevLogTerm:
			return False
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
	self.lastLogTerm = sender.log[lastLogIndex].term

class RequestVoteResponse(Message):

	def __init__(self, sender, RequestVote, vote_granted):
		Message.__init__(self, sender, AppendEntries.leaderID)
		self.term = sender.current_term
		#reply false if msg term < current term
		#if have not voted for anyone, and candidates log is at least asup to date
		#then grant vote
		self.vote_granted = vote_granted
			



