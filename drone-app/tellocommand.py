#!/usr/bin/python3

"""
@brief      This is program for commandeer Tello.
@author     Yiğit GÜMÜŞ
@date       01-06-2023
"""

import threading
import socket

class TelloCommand:
    def __init__(self):
        """
        @brief  Tello IP address. Use local IP address since 
                host computer/device is a WiFi client to Tello.
        """
        try:
            last_ip = open('last_ip.txt', 'r').read()
            if last_ip not in [None, '']:
                tello_ip = f"{last_ip}"
            else:
                
                tello_ip = input("Give DRONE_IP: ")
        except FileNotFoundError as err:
            print("File: 'last_ip.txt' not found!")
            
        """
        Tello port to send command message.
        """
        command_port = 8889
        """
        @brief  Host IP address. 0.0.0.0 referring to current 
                host/computer IP address.
        """
        host_ip = "0.0.0.0"

        """
        @brief  UDP port to receive response msg from Tello.
                Tello command response will send to this port.
        """
        response_port = 9000

        # self defines
        self.tello_ip = tello_ip
        self.command_port = command_port
        self.host_ip = host_ip
        self.response_port = response_port

        """ Welcome note """
        print("\n===Tello Command Program Initialize...===\n")
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host_ip, response_port))  # Bind for receiving

    def terminate(self):
        self._running = False
        self.sock.close()

    def recv(self):
        """ Handler for Tello response message """
        while self._running:
            try:
                msg, _ = self.sock.recvfrom(1024)  # Read 1024-bytes from UDP socket
                print("response: {}".format(msg.decode(encoding="utf-8")))
            except Exception as err:
                print(err)

    def send(self, msg):
        """ Handler for send message to Tello """
        msg = msg.encode(encoding="utf-8")
        self.sock.sendto(msg, (self.tello_ip, self.command_port))
        print("message: {}".format(msg))  # Print message

if __name__ == "__main__":
    """ Start new thread for receive Tello response message """
    t = TelloCommand()
    recvThread = threading.Thread(target=t.recv)
    recvThread.start()
    # komut alma moduna otomatik geçtirtiyor
    t.send("command")
    while True:
        try:
            # Get input from CLI
            msg = input("tello-cmd> ")
            t.send(msg)

            # Check for "end"
            if msg == "exit":
                t.terminate()
                recvThread.join()
                print("\nGood Bye\n")
                break
        except KeyboardInterrupt:
            print("EXITING...")
            t.terminate()
            recvThread.join()
            break
