#Main While Loop

#create three servers
#create global message queue
#sending message adds to the queue
#after every while loop, the class dispatches messages to server queue
#from server import Server, State
#from message import message
from queue import Queue
from random import randint
import time
import threading
import pudb
import pdb
import logging


#import logging and debugging 
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

from server import Server, State
from client import Client
from message import Msg_Type

#add methods to get global queue, 

class Raft:

	def __init__(self, number_servers=3):
		self.number_servers = number_servers
		self.rlock = threading.RLock()
		self.server_nums = self.get_server_ids(number_servers)
		#self.message_queue = Queue()
		self.message_queue = list()
		self.server_dict = {num: Server(num, self) for num in self.server_nums}
		self.client = Client(self)
		self.Run = True


	@property 
	def server_list(self):
		return tuple(self.server_dict.values())

	def get_server_ids(self, number_servers):
		server_nums = [str(randint(0,100000000000000)) for r in range(number_servers)]
		
		while len(server_nums) != len(set(server_nums)):
			self.get_server_ids(number_servers)
		return server_nums

	def distribute_message(self, msg, server_id):
		with self.rlock:
			#server.queue_messages.put(msg)
			logging.debug("Message Type %s"%type(msg).__name__)
			logging.debug("Message from %s"%msg.senderID)
			logging.debug("Message t0 %s" %msg.recipients)
			if msg.type ==  Msg_Type.FindLeader:
				print("FINDING LEADER")

			self.server_dict[server_id].queue_messages.append(msg)


	def main_loop(self):
		#update the timers for all the servers
		count = 0
		while self.Run and count < 5:
			logging.debug("COUNT %s" %count)
			[s.update_timers() for s in self.server_list]
			#distribute the messages for each server and message in the list
			#need to think of a better way to distribute messages
	
			while len(self.message_queue) > 0:
				logging.debug(len(self.message_queue))
				msg = self.message_queue.pop(0)
			
				logging.debug("Main distributing messages")
				[self.distribute_message(msg, serv) for serv in msg.recipients]
		
		
				
			logging.debug("Main Checking Messages")
			#change to a for loop
			for serv in self.server_list:
				serv.check_messages()
			
			count += 1
	
	def main_threads(self):
		#call start on threads
		count = 0
		for serv in self.server_list:
			serv.start()
		self.client.start()
		
		while self.Run and count < 1000000:
			with self.rlock:
				if len(self.message_queue)>0:
					print("count %s"%count)
					print(len(self.message_queue))
				for msg in self.message_queue:
					for serv in msg.recipients:
						self.distribute_message(msg, serv)
				del self.message_queue[:]
			with self.rlock:
				count +=1
				# for server in self.server_list:
				# 	if server.state == State.leader:
				# 		print("Count %s"%count)
						#pdb.set_trace()
						#self.end_program()


	def end_program(self):
		self.Run = False



if __name__ == '__main__':

	new_test = Raft(3)
	#new_test.main_loop()
	new_test.main_threads()


#Create global queue for messages
# while loop that gets message in queue, if type is something and recipient, 
#adds to that message queue
