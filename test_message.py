#Basic Tests for message class
import unittest
from message import Message, AppendEntries, AppendEntriesResponse, RequestVote, RequestVoteResponse
from server import Server, Msg_Type, State
from log import LogEntry, Log 
from raft import Raft

class test_message(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.testRaft = Raft(3)
		self.main_server_id = self.testRaft.server_nums[0]
		self.main_server = self.testRaft.server_dict[self.main_server_id]


	def test_message(self):
		msg = Message(self.main_server, "all servers")

		self.assertEqual(msg.senderID, self.main_server_id)
		self.assertEqual(len(msg.recipients), 2)

	def test_AppendEntries(self):
		entry1 = LogEntry(0, 1)
		self.main_server_id.log.append[entry1]
		msg = AppendEntries(self.main_server, "all servers")
		self.assertEqual(msg.senderID, self.main_server_id)
		self.assertEqual(msg.prevLogIndex, 1)



if __name__ == '__main__':
	unittest.main()
