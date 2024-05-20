import socket
import cv2
import pickle
import struct
import threading

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

ser_sock.bind(socket_address)
ser_sock.listen(5)

print(f"Server Serving at {ser_sock}")
client_connected = False
while 1:
    
    # client, addr = ser_sock.accept()
    # print(f"Client{client}")
    # print(f"Connected to Client@{addr}")
    # # if not client:
    # vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
    # while True:
    # # print(f"Connected to Client@{addr}")
    #     img, frm = vid.read()
    #     cv2.imshow('Server Side', frm)
    #     key = cv2.waitKey(1) & 0xff
    #     if client:
    #         break
    # # print(client)
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
    if not client_connected:
        # Пока клиент не подключен, транслировать видео
        vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
        while True:
            img, frm = vid.read()
            cv2.imshow('Server Side', frm)
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break

        # Проверяем, подключен ли клиент
        client, addr = ser_sock.accept()
        print(f"Client{client}")
        print(f"Connected to Client@{addr}")
        client_connected = True

    else:
        # После подключения клиента, передавать данные
        vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
        while True:
            img, frm = vid.read()
            a = pickle.dumps(frm)
            message = struct.pack("Q", len(a)) + a
            client.sendall(message)
            cv2.imshow('Server Side', frm)
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                client.close()
                client_connected = False
                break





# def get_ip_address():
#   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   s.connect(("8.8.8.8", 80))
#   return s.getsockname()[0]

# def video_stream(client,vid):
#     # vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#     while True:
#         ret, frm = vid.read()
#         if not ret:
#             break
#         a = pickle.dumps(frm)
#         message = struct.pack("Q", len(a)) + a
#         client.sendall(message)

# def video_display():
#     vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#     while True:
#         ret, frm = vid.read()
#         if not ret:
#             break
#         cv2.imshow('Server Side', frm)
#         key = cv2.waitKey(1) & 0xff
#         if key == ord('q'):
#             cv2.destroyAllWindows()
#             break

# # Socket creation
# ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host_ip = get_ip_address()
# print(f"Server IP Address: {host_ip}")

# port = 9999
# socket_address = (host_ip, port)

# ser_sock.bind(socket_address)
# ser_sock.listen(5)

# print(f"Server Serving at {ser_sock}")

# while True:
#     client, addr = ser_sock.accept()

#     print(f"Connected to Client@{addr}")

#     if client:
#         vid = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#         video_thread = threading.Thread(target=video_stream, args=(client,vid))
#         display_thread = threading.Thread(target=video_display, args=(vid))
#         video_thread.start()
#         display_thread.start()



