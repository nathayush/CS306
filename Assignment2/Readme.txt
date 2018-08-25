------------------------------------------------
Assignment: Server/Client socket programming
By: Ayush Nath
Date: 20 November, 2017
------------------------------------------------

Server input:
The server takes input of the events from a text file with structure as follows:
    <event name>
    <comma separated tags>
    <date dd/mm/yyyy>
    <event name>
    <comma separated tags>
    <date dd/mm/yyyy>
    ...

Starting the server:
    1. Unpack server.py
    2. Run server.py with Python 3.x, and with input file name and port as first and second argument respectively.
        USAGE: "python3 server.py server-input.txt 1234"
    3. Note down the server IP address printed in the first line.
    4. Multi-threaded server is now listening for hosts/queries.

Starting the client:
    1. Unpack client.rar
    2. Run client.exe
    3. Use the GUI to interact with the server.
    
NOTE: Always start the server before starting the client socket.

