import socket
import cv2
import pickle
import struct
import threading
import select

def get_ip_address():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  return s.getsockname()[0]

# Socket creation
ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = get_ip_address()
print(f"Server IP Address: {host_ip}")

port = 9999
socket_address = (host_ip, port)
ser_sock.settimeout(0.2)
ser_sock.bind(socket_address)
ser_sock.listen(1)

print(f"Server Serving at {ser_sock}")
client = None
vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
while True:
    # vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
    ready_to_read, _, _ = select.select([ser_sock], [], [], 0)
    if ready_to_read:  # If there is a new connection
        client, addr = ser_sock.accept()
        print(f"Connected to Client@{addr}")
    if client:  # If a client is connected
         cv2.destroyAllWindows()
         while True:
            try: 
                img, frm = vid.read()
                a = pickle.dumps(frm)
                message = struct.pack("Q", len(a)) + a
                client.sendall(message)
            except Exception as e:
                print(f"Error: {e}")
                client.close()
                client = None
                break


    else:  # If no client is connected
        img, frm = vid.read()
        cv2.imshow('Server Side', frm)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        if client:
            client.close()
        break


# while True:
#     try:
#         client, addr = ser_sock.accept()
#         print(f"Connected to Client@{addr}")
#         if client:
#             vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
        
#             while True:
#                 img, frm = vid.read()
#                 a = pickle.dumps(frm)
#                 message = struct.pack("Q", len(a)) + a
#                 client.sendall(message)
#                 # cv2.imshow('Server Side', frm)
#                 # key = cv2.waitKey(1) & 0xff
#                 # if key == ord('q'):
#                     # client.close()
#                     # break
#     except socket.timeout:
#         # pass
#     # print(f"Client{client}")
#     # print(f"Connected to Client@{addr}")
#     # # if not client:
#         vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#         while True:
    
#             img, frm = vid.read()
#             cv2.imshow('Server Side', frm)
#             key = cv2.waitKey(1) & 0xff
#             if key == ord('q'):
#                 break
    # print(client)
    # print(f"Connected to Client@{addr}")
    # if client:
    #     # show_image = True
    #     vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
    #     # while(vid.isOpened()):
    #     while True:
    #         img, frm = vid.read()
    #         a = pickle.dumps(frm)
    #         message = struct.pack("Q", len(a)) + a
    #         client.sendall(message)
    #         cv2.imshow('Server Side', frm)
    #         key = cv2.waitKey(1) & 0xff
    #         if key == ord('q'):
    #             client.close()

# def accept_connections():
#     while True:
#         try:
#             client, addr = ser_sock.accept()
#             print(f"Connected to Client@{addr}")
#             # здесь вы можете обрабатывать соединение с клиентом
#         except socket.timeout:
#             pass

# def read_video():
#     vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#     while True:
#         img, frm = vid.read()
#         cv2.imshow('Server Side', frm)
#         key = cv2.waitKey(1) & 0xff
#         if key == ord('q'):
#             break

# # запускаем потоки
# threading.Thread(target=accept_connections).start()
# threading.Thread(target=read_video).start()