#!/usr/bin/python3

"""
@brief      This is program for stream video from Tello camera.
@author     Yiğit GÜMÜŞ
@date       01-06-2023
"""

import threading
import cv2


class TelloStream:
    def __init__(self):
        """ Welcome note """
        print("\n===Tello Video Stream Program Initialize...===\n")

        self._running = True
        self.video = cv2.VideoCapture("udp://@0.0.0.0:11111")

    def terminate(self):
        self._running = False
        self.video.release()
        cv2.destroyAllWindows()

    def recv(self, countID):
        """ Handler for Tello states message """
        while self._running:
            try:
                ret, frame = self.video.read()
                if ret:
                    # Resize frame
                    height, width, _ = frame.shape
                    new_h = int(height / 2)
                    new_w = int(width / 2)

                    # Resize for improved performance
                    new_frame = cv2.resize(frame, (new_w, new_h))

                    # Display the resulting frame
                    cv2.imwrite('img', new_frame)
                # Wait for display image frame
                # cv2.waitKey(1) & 0xFF == ord('q'):
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.terminate()
            except Exception as err:
                print(err)

if __name__ == "__main__":
    """ Start new thread for receive Tello response message """
    t = TelloStream()
    recvThread = threading.Thread(target=t.recv)
    recvThread.start()

    while True:
        try:
            # Get input from CLI
            msg = input("tello-strem> ")

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
