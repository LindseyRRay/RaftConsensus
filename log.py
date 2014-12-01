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
	def __init__(self):
		self.log = list()
		self.CommitIndex = 0
		self.prevLogIndex = 0

	@property
	#index of last log entry
	def lastLogIndex(self):
	    return len(self.log)

	#index of last log entry preceeding new ones
	def incrementprevLogIndex(self):
		self.prevLogIndex +=1	

	    
	