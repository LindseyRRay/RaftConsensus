import unittest
from server import Server
from raft import Raft 

class Test_Server(unittest.testcase):

	def test_send_message(self):	
		new_test = Raft(3)
		#new_test.main_loop()
		new_test.main_threads()
		