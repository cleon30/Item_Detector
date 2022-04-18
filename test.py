import cv2

import qr_extractor as reader


frame = cv2.imread('qr_code.jpg')

codes, new_frame = reader.extract(frame, True)
#cv2.imshow("frame", new_frame)
print(codes)

# When everything done, release the capture
