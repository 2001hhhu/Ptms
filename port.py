import socket
import sys
import time

class Pp:

    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR,1)

            self.s.blind(('0.0.0.0',8080))
            self.s.listen(10)
        except socket.error as msg:
            print("Failed to create socket. Error code:"  + str(msg[0]) + " , Error message :"  + msg[1])
            sys.exit(1);
        print("Wait for Connection......")


    def detect(self):
        while(True):
            sock,add = self.s.accept()
            buf = sock.recv(1024)
            print("The data from" + str(addr[0]) + "is" + str(buf))
            print("Successfullly")
            socket.close()

    def recovery_listening(self):
        while 10:
            time.sleep(5)
        detect()
