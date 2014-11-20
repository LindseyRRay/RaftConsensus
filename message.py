#Message Class
types = ['RFV_YES', 'RFV', 'HEARTBEAT']
#Import list of ServerIDS

from enum import Enum 


class Msg_Type(Enum):
	HEARTBEAT = 1
	RFV = 2
	RFV_YES = 3



class Message:
	
	def __init__(self, sender, recipients, msg_type, term, server_ids):
		self.sender = sender
		self.SERVER_IDS = server_ids
		self.recipients = self.parse_recipients(recipients)
		self.type = msg_type
		self.term = term
		

	def parse_recipients(self, recipients):
		#if recipients are all servers
		if recipients[0] == 'a':
			list_recipients = [str(server) for server in self.SERVER_IDS if server != self.sender]
			return list_recipients
		else:
			#str_recipients = [str(recip) for recip in recipients]
			#list_recipients = [server for server in self.SERVER_IDS if server in str_recipients]
			return recipients
		
				

