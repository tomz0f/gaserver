#!/usr/bin/python3
"""
@brief      This is program for stream sensor states from Tello.
@author     Yiğit GÜMÜŞ
@date       01-06-2023
"""

import threading
import socket

class TelloState:
    def __init__(self):
        """
        @brief  Host IP address. 0.0.0.0 referring to current 
                host/computer IP address.
        """
        host_ip = "0.0.0.0"

        """
        @brief  UDP port to receive response msg from Tello.
                Tello command response will send to this port.
        """
        response_port = 8890

        """ Welcome note """
        print("\n === Tello Sensor States Program Initialize...===\n")

        self.state = {}
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host_ip, response_port))  # Bind for receiving

    def terminate(self):
        self._running = False
        self.sock.close()

    def recv(self):
        """ Handler for Tello states message """
        while self._running:
            try:
                msg, _ = self.sock.recvfrom(1024)  # Read 1024-bytes from UDP socket
                msg = msg.decode(encoding="utf-8").split(';')
                for i in msg:
                    k,v = i.split(":")
                    self.state[k] = v

            except Exception as err:
                print(err)
            except KeyboardInterrupt:
                self.terminate()
    

if __name__ == "__main__":
    """ Start new thread for receive Tello response message """
    t = TelloState()
    recvThread = threading.Thread(target=t.recv)
    recvThread.start()

    while True:
        try:
            # Get input from CLI
            msg = input("tello-sensor> ")

            # Check for "end"
            if msg == "exit":
                t.terminate()
                recvThread.join()
                print("\nGood Bye\n")
                break
        except KeyboardInterrupt:
            t.terminate()
            recvThread.join()
            break
