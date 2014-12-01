import unittest
from server import Server, State
from raft import Raft 
from message import Msg_Type, Message, FindLeader, ClientRequest, FindLeaderResponse, ClientRequestResponse
import pdb 


class Test_Server(unittest.TestCase):

	def setUp(self):
		self.new_raft = Raft(3)
		#create ref to server
		self.serv_id = self.new_raft.server_nums[0]
		self.serv = self.new_raft.server_dict[self.serv_id]

	def test_client_req(self):
		self.serv.state = State.leader
		msg = ClientRequest(self.serv_id, 1)
		self.serv.queue_messages.append(msg)
		self.serv.check_messages()
		self.assertEqual(self.serv.log.log[0].term, self.serv.current_term)
		self.assertEqual(len(self.new_raft.message_queue), 1)
		self.assertEqual(self.new_raft.message_queue[0].type, Msg_Type.AppendEntries)



if __name__ == '__main__':
	unittest.main()
		
		