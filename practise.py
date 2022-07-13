'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

'''
import os
import sys
import socket
import mimetypes
import subprocess
import multiprocessing

class HTTPServer:

    def __init__(self,ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((ip,port))
        sock.listen()
        while True:
            out = ""
            print("Waiting for a connection")
            connection,client_address=sock.accept()
            recv =connection.recv(10000).decode()
            sl = recv[5:]
            space_index = sl.index(' ')
            format1 = sl[:space_index]

            if format1 == None or space_index == 0:
                out = "<a href="+"ComputerSystems-p4"+">"+"ComputerSystems-p4"+"</a><br>"
                headers = "HTTP/1.1 200 OK\nContent-Type :text/html\nContent-Length :1000\n\n"
                out = out.encode()
            
            elif format1 == "ComputerSystems-p4":
                for file in os.listdir(r"C:\Users\HP\OneDrive\Desktop\MSIT\CS\Project-2\ComputerSystems-p4"):
                    out += "<a href="+str(file)+">"+str(file)+"</a><br>"
                headers = ("HTTP/1.1 200 OK\nContent-Type :text/html\nContent-Length :1000\n\n")
                out = out.encode()

            elif format1 == "bin":
                for file in os.listdir('bin'):
                    f = os.path.join('bin', file)
                    if os.path.isfile(f):
                        out += "<a href="+str(file)+">"+str(file)+"</a><br>"
                headers = "HTTP/1.1 200 OK\nContent-Type :text/html\nContent-Length :1000\n\n"
                out = out.encode()
               
            elif format1 == 'ls' or format1 == 'du':
                out = os.popen('dir').read().encode()
                headers = "HTTP/1.1 200 OK\nContent-Type :text/html\nContent-Length :1000\n\n"

            elif format1 == 'www':
                for file in os.listdir('www'):
                    f = os.path.join('www', file)
                    if os.path.isfile(f):
                        out += "<a href="+str(file)+">"+str(file)+"</a><br>"
                headers = "HTTP/1.1 200 OK\nContent-Type :text/html\nContent-Length :1000\n\n"
                out = out.encode()

            elif format1 == 'test.py':
                f = os.path.join('bin', format1)
                typ1 = (mimetypes.MimeTypes().guess_type(str(format1))[0])
                sub = subprocess.run([sys.executable, "-c", open(str(f)).read()], capture_output=True, text=True)
                out = sub.stdout.encode()
                #print(out)
                headers = "HTTP/1.1 200 OK\nContent-Type :"+str(typ1)+"\nContent-Length :"+str(len(out))+"\n\n"
 
            else:
                if format1 in os.listdir('www'):
                    typ1 = (mimetypes.MimeTypes().guess_type(str(format1))[0])
                    f = os.path.join('www', format1)
                    out = open(f, 'rb').read()
                    headers = "HTTP/1.1 200 OK\nContent-Type :"+str(typ1)+"\nContent-Length :"+str(len(out))+"\n\n"
                else:
                    out = "<h1> 404 PAGE NOT FOUND </h1>".encode()
                    headers = "HTTP/1.1 404 OK\nContent-Type :text/html\nContent-Length :"+str(len(out))+"\n\n"
            connection.sendall(headers.encode()+out)

def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    p1 = multiprocessing.Process(target=HTTPServer, args=('127.0.0.1', 8888, ))
    p1.start()
    p1.join()
    print("done")

if __name__ == "__main__":
    main()
