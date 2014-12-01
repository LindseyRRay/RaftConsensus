#Write client class
#client class responsible for sending log entries to leader
#client talks to random server, server sends back leader id once confirmed
#client then sends commands with terms

#implement match index checking for leaders

from message import ClientRequest, FindLeader, FindLeaderResponse, ClientRequestResponse

class Client(Threading.thread):
	
	def __init__ (self, raft_instance):
		Threading.thread.__init__(self)
		self.raft_instance = raft_instance
		self.commands = list()
		self.commitIndex = 0
		self.message_queue = list()
		self.rlock = threading.RLock()
		self.currentLeader = None
		self.leaderIndex = 0


	def find_leader(self):
		#send message to each server in list
		with self.rlock:
			for server in self.raft_instance.server_nums:
				self.raft_instance.server_dict[server].queue_messages.append(FindLeader(server))
	
	def process_request_response(self, msg):
		#update commit index when leader communicates command has been committed to state machine


	def process_leader_response(self, msg):
		if msg.data:
			self.currentLeader = msg.sender
			self.leaderIndex += 1

	def process_messages(self):
		with self.rlock:
			for msg in self.message_queue:
				if msg.type == Msg_Type.FindLeaderResponse:
					self.process_leader_response(msg)
				elif msg.type == Msg_Type.ClientRequestResponse:
					self.process_request_response(msg)


	def send_command(self, command):
		with self.rlock:
			if self.leaderIndex = len(self.commands):
				client_req = ClientRequest(command)
				self.raft_instance.server_dict[server].queue_messages.append(client_req)
				self.commands.append(command)
			else:
				self.find_leader()
				self.send_command(command)


