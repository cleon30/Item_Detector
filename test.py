import cv2

import qr_extractor as reader


frame = cv2.imread('ROI_26.png')

codes, new_frame = reader.extract(frame, True)
cv2.imshow("frame", new_frame)
cv2.waitKey()
#print(codes)

# When everything done, release the capture
