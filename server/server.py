import socket, traceback

"""
Create a UDP socket binding to the specified port and poll the socket for incoming data.
"""

host = ''
port = 50000

# Create a datagram (UDP) socket
# to communicate over IPv4 (AF_INET)
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Not sure if reuse of port and broadcast mode really required as of now
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the IP address and port number to socket instance
s.bind((host, port))

print("Success binding: UDP server up and listening")

while 1:
    try:
        # Buffer size 1024
        message, address = s.recvfrom(1024)
        message_string = message.decode("utf-8")
        print (message_string)
        
    except (KeyboardInterrupt, SystemExit):
        raise traceback.print_exc()
