#Message Class
types = ['RFV_YES', 'RFV', 'HEARTBEAT']
#Import list of ServerIDS
from raft import SERVER_IDS


class Message:
	
	def __init__(self, sender, recipients, msg_type, term):
		self.sender = sender
		self.recipients = self.parse_recipients(recipients)
		self.type = msg_type
		self.term = 

	def parse_recipients(self, recipients):
		#list_recipients = list()
		if recipients == 'all servers':
			list_recipients = [server for server in SERVER_IDS if server != self.sender]
		else:
			list_recipients = [server for server in SERVER_IDS if server in recipients]

		return list_recipients
				

