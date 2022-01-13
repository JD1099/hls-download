from termcolor import colored
from scp import SCPClient
import time, os, sys, validators, random, string

if sys.platform == "linux":
	dataPath = "/tmp/hls-download/"
if sys.platform == "win32":
	dataPath = "C:/tmp/hls-download/"

if os.path.isdir(dataPath) == True:
	pass
else:
	os.mkdir(dataPath)

def sendTickets(fileName=' '):

	ticket = str(dataPath + fileName)
	if fileName == ' ':
		for fileName in os.listdir(dataPath):
			ticket = str(dataPath + fileName)
			#print('\nscp "%s" "%s:%s"' % (ticket, "server100", "/tmp/hls-download/" + fileName))
			os.system('scp "%s" "%s:%s"' % (ticket, "server100", dataPath) )
			os.remove(dataPath + fileName)
	else: 
		
		os.system('scp "%s" "%s:%s"' % (ticket, "server100", dataPath) )
		os.remove(dataPath + fileName)

def clear():
	os.system("cls" if os.name == "nt" else "clear")

def userPickTicketIndex():
	if len(os.listdir(dataPath)) == 0:
		print('Ticket storage is empty!')
		print(colored('Abort!','red'))
		time.sleep(1.5)
	else:
		index = 0
		indexList = []
		print('Please select a ticket:')
	
		for fileName, element in enumerate(os.listdir(dataPath)):
			print("{}) {}".format(fileName+1,element))
			index = index + 1
			indexList.extend([element[fileName]])
		i = input('\nSelect a ticket to send or type "delete" to clear storage: ')
		if str(i) == "delete":
			confirm = input('Are you sure you want to delete all tickets? Type "yes" to confirm: ')
			if	confirm == "yes":
				for fileName in os.listdir(dataPath):
					os.remove(dataPath + fileName)
				print('Tickets deleted')
				time.sleep(1.5)
			
				
		else:
			global ticket
			ticket = str(dataPath + element) 
			confirm = input('Do you want to delete this ticket? Type "yes" to confirm: ')
			if	confirm == "yes":
				os.remove(ticket)
				print('Ticket deleted')
			else:
				print('\nTicket selected: '+ element)
				sendTickets(element)
				time.sleep(1.5)
			
			

def createTicket():
	while True:  # asks the user input then validates the input.
		hlsRequest = input("please insert hls stream url: ")
		print("checking url...")
		time.sleep(0.25)
		if validators.url(hlsRequest):

			print(colored("url:", "white"), colored("valid", "green"))
			break
		else:

			print(colored("url:", "white"), colored("invalid", "red"))
			print("please try again")
			time.sleep(0.25)
			pass

	while True:  # asks for more user input then validates it again.

		fileName = input("please insert a name for this file: ")
		print("checking filename...")
		time.sleep(0.25)
		if fileName.find("/") == -1:
			print(colored("filename:", "white"), colored("valid", "green"))
			break
		else:
			print(colored("filename:", "white"), colored("invalid", "red"))
			print("filename cannot contain forward slash")


	# data = {"hlsRequest" : hlsRequest, "fileName" : fileName}
	data = {}
	data["hlsRequest"] = hlsRequest
	data["fileName"] = fileName
	
	if len(fileName) > 128:
		fileName = fileName[0:128] + ' '
	else:
		fileName = fileName + ' '
		
	fileName = fileName.replace('.',' ')
	fileName = fileName.replace('/',' ')
	randNumb = "".join(random.choice(string.digits) for i in range(16))  # generates a random 16 digit number.
	
	
	print(dataPath + fileName)
	file = open(dataPath + fileName + str(randNumb), "w")
	file.write("data " + "= " + str(data))
	file.close()
	
	clear()
	ticket = str(dataPath + fileName)
	print('Ticket created')
	time.sleep(1)


options = {}
#	 [USER OPTION] = PROGRAM RESULT
options['Create new ticket [default]'] = '1'
options['Send ticket from storage'] = '2'
options['Send all tickets to server'] = '3'
options['Quit'] = '4'
def selectFromDict(options, name):

	index = 0
	indexValidList = []
	print('\nPlease select an option: \n')
	for optionName in options: # crating an index of options for the user
		index = index + 1
		indexValidList.extend([options[optionName]])
		print(str(index) + ') ' + optionName) # printing the index
	inputValid = False
	while not inputValid:	# input loop until input is valid
		inputRaw = input('\n' + name + ': ')
		try:
			inputNo = int(inputRaw) - 1
		except:
			inputNo = int(0)
		if inputNo > -1 and inputNo < len(indexValidList): # input is valid when the user input is more than
			selected = indexValidList[inputNo]			   # -1 and less than the length of the index
			#print('Selected ' +  name + ': ' + selected) commented out line
			inputValid = True
			break
		else:
			print('Please select (2) or press enter for default')
	clear()
	if inputNo == 1:
		userPickTicketIndex()
	
	elif inputNo == 2:
		print('Sending tickets!\n')
		sendTickets()
		time.sleep(1)
	
	elif inputNo == 3:
		quit()
	
	else:
		print('Lets create a new hls ticket!\n')
		createTicket()
		
	return selected

while True:
	clear()

	print("hello")
	print("time:", time.asctime())
	print("system:", sys.platform)
	print("working directory: " + str(dataPath))

	selectFromDict(options, 'Press enter for default')	

quit()
