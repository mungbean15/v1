# File with exceptions related to client


'''
Ensures correct number of arguments and port numbers are integers
Arguments:
    <argv> - array of command line arguments
'''
def c_check_arguments(argv):
    if len(argv) != 4:
        print("Error usage: python3 client.py <server_IP> <server_port> <client_udp_server_port>\n")
        exit(0)

    try:
        int(argv[2])
    except:
        print("Error usage: Argument <server_port> must be an integer.\n")
        exit(0)
    
    try:
        int(argv[3])
    except:
        print("Error usage: Argument <client_udp_server_port> must be an integer.\n")  
        exit(0)


'''
Ensure that the server_port is within the range [1024, 65535]
Arguments:
    <serverPort> - the server_port user wants to use
'''
def c_check_server_port(server_port):
    if server_port < 1024 or server_port > 65535:
        print("Error input: Argument <server_port> must be a value in range [1024, 65535].\n")
        exit(0)

'''
Ensure that the client_udp_server_port is within the range [1024, 65535]
Arguments:
    <UDPPort> - the client_udp_server_port user wants to use
'''
def c_check_UDP_port(UDP_port):
    if UDP_port < 1024 or UDP_port > 65535:
        print("Error input: Argument <client_udp_server_port> must be a value in range [1024, 65535].\n")
        exit(0)