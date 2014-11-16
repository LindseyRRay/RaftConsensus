#Main While Loop

#create three servers
#create global message queue
#sending message adds to the queue
#after every while loop, the class dispatches messages to server queue
from server import Server, State
from message import message
from queue import Queue
from random import randint
from time import time

class Raft:

	def __init__(self, number_servers=3):
		self.number_servers = number_servers
		self.server_nums =self.get_server_ids(number_servers)
		self.server_list = [Server(r) for r in server_nums]
		self.message_queue = Queue()
		self.Run = True

	def get_server_ids(self, number_servers):
		dups = False
		while dups == False:
			servers_nums = [randint(0,100) for r in range(number_servers)]
			if len(server_nums) != len(set(server_nums)):
				dups = True
		return server_nums 



	def main_loop(self):
		




	def end_program(self):
		self.run = False




def main():


#Create global queue for messages
# while loop that gets message in queue, if type is something and recipient, 
#adds to that message queue
