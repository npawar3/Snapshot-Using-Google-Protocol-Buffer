import sys
sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

import bank_pb2
import socket
import time

import random


branches = {}
branch_name = []

def initBranch(fname,total_balance):
  
	count=0
	BR = bank_pb2.BranchMessage()
  
  
	with open(fname) as f:
		for line in f:  
        
			#print line
			ip = line.split()[1]    
			port = line.split()[2]  
			inport=int(port.strip('\0'))      
			bank=BR.init_branch

			branch1=bank.all_branches.add()

			branch1.name=line.split()[0]
			branch1.ip=ip
			branch1.port=inport
			count=count+1


			temp_list = []
			temp_list.append(ip)
			temp_list.append(inport)
			branches[line.split()[0]] = temp_list
			
			branch_name.append(line.split()[0])
  
	f.close()

  
    
	bank.balance = int(total_balance) / count
    
	with open(fname) as f:
		for line in f:
	
			ip = line.split()[1]    
			port = line.split()[2]  
			inport=int(port.strip('\0'))

			try:

				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				s.connect((ip,int(inport)))
				ip, port = s.getsockname()
				print 'socket : ' + str(s) + ' ip : ' + str(ip) + ' port is ' + str(port)
				s.send(BR.SerializeToString())
				print s.recv(1024)

				s.close()
			except:
				print "Not able to connect to " + line + " " +str(sys.exc_info()[0])
				sys.exit(0)

          
          
	f.close()


	
	




def initSnapshot():
	
	snapshot_id = 1
		
	while snapshot_id <= 10:
		branch = random.choice(branch_name)
		ip = branches[branch][0]
		port = branches[branch][1]
	
		branch_message = bank_pb2.BranchMessage()
		init_snapshot = branch_message.init_snapshot
		init_snapshot.snapshot_id = snapshot_id
	

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((ip,int(port)))
	
		s.send(branch_message.SerializeToString())
		print s.recv(1024)

		s.close()
	
		RetrieveSnapshot(snapshot_id)


		snapshot_id += 1




def RetrieveSnapshot(id):
	time.sleep(3)
	#Create Retrieve Message
	branch_message = bank_pb2.BranchMessage()
	retrieve_snapshot = branch_message.retrieve_snapshot
	retrieve_snapshot.snapshot_id = id

	print "Snapshot id ", id
	for branch_name in branches:
		
		ip = branches[branch_name][0]
		port = branches[branch_name][1]
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((ip,int(port)))
		s.send(branch_message.SerializeToString())
		snapshot = s.recv(1024)
		recv_message = bank_pb2.BranchMessage()
		recv_message.ParseFromString(snapshot)
		print 'Snapshot returned from ' + branch_name + " : " + str(recv_message)
		s.close()
		


if __name__ == '__main__':

	if len(sys.argv) != 3:
	        print "Invalid Parameters: <Total Balanace> <branches.txt>"
	        sys.exit(0)
	else:
	        total_balance = sys.argv[1]
	        fname = sys.argv[2]

	initBranch(fname,total_balance)
	time.sleep(5)
	initSnapshot()
