#
#
# McMaster University
# SE4C03 - Assignment 1
# Aimal Khan
# D'Arcy Rail-Ip
# Diego Valdivia
#
#

import sys
from socket import *

# Sort arguments and determine if using SSL
if len(sys.argv) == 4 and str(sys.argv[1]) == '-s':
    email_recepient = str(sys.argv[2])
    mailserver = str(sys.argv[3])
    port = 587
    import ssl
    import base64
    import getpass
elif len(sys.argv) == 3:
    email_recepient = str(sys.argv[1])
    mailserver = str(sys.argv[2])
    port = 25
else:
    print "Arguments invalid."
    sys.exit(0)

# Receive email sender from command line
email_sender = raw_input("Enter the sender's email address:")

if str(sys.argv[1]) == '-s':
    email_sender_password = getpass.getpass("Enter the sender's email password:")

# Receive message from command line
print "Enter your email message below. Write a '.' and press enter to finish."
email_body = ""
user_input = ""


# Loop until hitting the "." character
while user_input != '.':
   user_input = raw_input()
   email_body += user_input + '\r\n'

# Create socket called clientSocket and establish a TCP connection
# with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))
response = clientSocket.recv(1024)
print response
if response[:3] != '220':
    print '220 reply not received from server.'

# Send HELLO command.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
response = clientSocket.recv(1024)
print response
if response[:3] != '250':
    print '250 reply not received from server.'

if str(sys.argv[1]) == '-s':
    # Send STARTTLS message to begin SSL connection
    start_tls_msg = "STARTTLS\r\n"
    clientSocket.send(start_tls_msg)
    response = clientSocket.recv(1024)
    print response

    # Create a SSL socket
    ssl_socket = ssl.wrap_socket(clientSocket)
    clientSocket = ssl_socket

    # Send HELLO command to new socket
    clientSocket.send(heloCommand)
    response = clientSocket.recv(1024)
    print response

    # Authorize credentials
    auth_msg = "AUTH LOGIN\r\n"
    clientSocket.send(auth_msg)
    response = clientSocket.recv(1024)
    print response

    # Send email username
    sender_msg = base64.b64encode(email_sender) + "\r\n"
    clientSocket.send(sender_msg)
    response = clientSocket.recv(1024)
    print response

    # Send email password
    sender_pass = base64.b64encode(email_sender_password) + "\r\n"
    clientSocket.send(sender_pass)
    response = clientSocket.recv(1024)
    print response

    # Verify credentials
    if response[:3] != "235":
        # If invalid, close connection and exit.
        print "Invalid credentials."
        quitmsg = "QUIT\r\n"
        clientSocket.send(quitmsg)
        response = clientSocket.recv(1024)
        print response
        sys.exit(0)
    
# Send MAIL FROM command and print server response.
from_msg = "MAIL FROM:<" + email_sender + ">\r\n"
clientSocket.send(from_msg)
response = clientSocket.recv(1024)
print response

# Send RCPT TO command and print server response.
rcpt_msg = "RCPT TO:<" + email_recepient + ">\r\n"
clientSocket.send(rcpt_msg)
response = clientSocket.recv(1024)
print response

# Send DATA command and print server response.
data_msg = "DATA\r\n"
clientSocket.send(data_msg)
response = clientSocket.recv(1024)
print response

# Send message data.
clientSocket.send(email_body)

# Send QUIT command and get server response.
quitmsg = "QUIT\r\n"
clientSocket.send(quitmsg)
response = clientSocket.recv(1024)
print response

