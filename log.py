#log class

class LogEntry:

	def __init__(self, term, command):
		self.term = term
		self.command = command
	# 	self.commit = False

	# def commit(self):
	# 	self.commit = True

	def __eq__(self, other_log):
		return (self.term == other_log.term and self.command == other_log.command)
		

class Log:
	#needs last log index, entry and prev log index and entry attributes
	def __init__(self, serverID):
		self.log = list()
		self.CommitIndex = 0
		self.serverID = None
		self.lastLogTerm = None

	#index of last log entry preceeding new ones
	#this must be leader manipulated
	def increment_prevLogIndex(self):
		self.prevLogIndex +=1

	def compare_up_to_date(self, msg):
		#safety property implemented in election restriction
		#if logs have last entries with different terms, then the log with the later term
		#is more up to date
		#if logs end with the same term, then the longest log is most up to date
		#returns tuple of boolean if logs are equal and them most up to date on
		if self.log[-1].term == msg.lastLogTerm and self.log.lastLogIndex == msg.lastLogIndex:
			return (True, None)
		else:
			if self.log.lastLogIndex > msg.lastLogIndex or self.log[-1].term > msg.lastLogTerm:
				return (False, self.serverID)
			else:
				return (False, msg.serverID)
	@property
	#index of last log entry
	def lastLogIndex(self):
	    return len(self.log)-1
	

	    
	