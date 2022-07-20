# cybernet
A python tool to control other computers remotely
This script is used to create a server that can be used to run a command on a remote computer.
It will listen on the port specified by the --port option.

# Requirements
Python 3.0+

# Usage
cybernet.py -t target_host -p port [options] 
-h --help                   - To print the help menu
-l --listen                 - Listen on [host]:[port] for incoming connections
-e --execute=file_to_run    - Execute the given file upon receiving a connection
-c --command                - initiate the command shell
-u --upload=destination     - Upload files and write to destination upon receiving a connection

# Example
./cybernet.py -t 123.4.5.6 -p 22 -l 456.7.8:24 -c 
