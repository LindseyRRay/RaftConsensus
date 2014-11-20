#Main While Loop

#create three servers
#create global message queue
#sending message adds to the queue
#after every while loop, the class dispatches messages to server queue
#from server import Server, State
#from message import message
from queue import Queue
from random import randint
from time import time
import threading
import pudb
import pdb

from server import Server, State

#add methods to get global queue, 

class Raft:

	def __init__(self, number_servers=3):
		self.number_servers = number_servers
		self.rlock = threading.RLock()
		self.server_nums = self.get_server_ids(number_servers)
		#self.message_queue = Queue()
		self.message_queue = list()
		self.server_list = [Server(r, self) for r in self.server_nums]
		self.Run = True

	def get_server_ids(self, number_servers):
		dups = True
		server_nums = []
		while dups == True:
			dups = False
			[server_nums.append(randint(0,100000000000000)) for r in range(number_servers)]
			if len(server_nums) != len(set(server_nums)):
				dups = True
		
		[str(num) for num in server_nums]
		print(server_nums)
		return server_nums

	def distribute_messages(self, msg, server):
		for recip in msg.recipients:
			if str(server.ID) == str(recip):
				with self.rlock:
					#server.queue_messages.put(msg)
					print("adding to queue")
					server.queue_messages.append(msg)
					print(server.queue_messages)

#	def generator_queue(self):
#		print(self.message_queue.qsize())
#		yield self.message_queue.get() 


	#def generator_queue(self):
	#	print(len(self.message_queue))
	#	yield self.message_queue.pop(0)

	def main_loop(self):
		#update the timers for all the servers
		count = 0
		while self.Run and count < 5:
			print("COUNT %s" %count)
			[s.update_timers() for s in self.server_list]
			#distribute the messages for each server and message in the list
			#need to think of a better way to distribute messages
	
			while len(self.message_queue) > 0:
				print(len(self.message_queue))
				msg = self.message_queue.pop(0)
			
				print("Main distributing messages")
				print("Message Type %s"%msg.type)
				print("Message from %s"%msg.sender)
				print("Message t0 %s" %msg.recipients)
				[self.distribute_messages(msg, serv) for serv in self.server_list]
				#pdb.set_trace()
		
				
			print("Main Checking Messages")
			[serv.check_messages() for serv in self.server_list]
			count += 1

			if count == 5:
				self.message_queue = list()

			#if self.message_queue.qsize() == 0:
			#	pudb.set_trace()
		

	def end_program(self):
		self.Run = False



if __name__ == '__main__':

	new_test = Raft(3)
	new_test.main_loop()



#Create global queue for messages
# while loop that gets message in queue, if type is something and recipient, 
#adds to that message queue
