This is a program to ensure reliable transmission in UDP connection, using Go back N algorithm

Run emulator using
./nEmulator-linux386 <recieving port for sender> <reciever address> <reciever recieving port> <recieving port for reciever> <sender address> <maximum delay> <packet discard prob> <verbose-Mode>

Run reciever using
python3 receiver.py <hostname for emulator> <ACK port for emulator> <port to recieve packet from emulator> <name of file to write output>

Run sender using
python3 sender.py <hostname for emulator> <port to send packet to emulator> <ACK port> <name of file to read>

run them in order of: emulator reciever sender
