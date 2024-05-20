import socket
import cv2
import pickle
import struct
import numpy as np 

def get_ip_address():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  return s.getsockname()[0]

# Socket creation
cln_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = get_ip_address()


print(f"Reciever IP {host_ip}")

port = 9999
socket_address = (host_ip, port)

cln_sock.connect(socket_address)

# dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2 #defining distance function
prevCircle = None

data = b""
payload_size = struct.calcsize("Q")
backSub = cv2.createBackgroundSubtractorMOG2()
backSub.setDetectShadows(False)
while True:
    while len(data) < payload_size:
        packet = cln_sock.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += cln_sock.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    #cv2
    frame = pickle.loads(frame_data)
    fg_mask = backSub.apply(frame)
    retval, mask_thresh = cv2.threshold( fg_mask, 100, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # Apply erosion
    mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)
    min_contour_area = 120
    contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    # print(contours)
    frame_out = frame.copy()
    for cnt in large_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        frame_out = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 3)
    frame_ct = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Client side", frame_out)
    # grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converting frame to grayscale
    # blueFrame = cv2.GaussianBlur(grayFrame, (17,17), 0) #blurring frame

    # circles = cv2.HoughCircles(blueFrame, cv2.HOUGH_GRADIENT, 1.2, 100,param1=100, param2=30, minRadius=75, maxRadius=400) #detecting circles
    
    # if circles is not None: 
    #     circles = np.uint16(np.around(circles)) #rounding circles
    #     chosen = None 
    #     for i in circles[0,:]: 
    #         if chosen is None: chosen = i 
    #         if prevCircle is not None: 
    #             if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) > dist(i[0], i[1], prevCircle[0], prevCircle[1]): 
    #                 chosen = i 
    #     #if distance between current circle and previous circle is less than distance between chosen circle and previous circle, set chosen circle to current circle
    #     cv2.circle(frame,(chosen[0],chosen[1]), 1, (0,100,100), 3) #draw circle point
    #     cv2.circle(frame,(chosen[0],chosen[1]), chosen[2], (255,0,0), 3) #draw circle
    #     prevCircle = chosen
    
    # cv2.imshow("circles", frame) #show frame
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
cln_sock.close()