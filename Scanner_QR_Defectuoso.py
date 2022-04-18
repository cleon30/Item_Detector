# Import the required toolkit
from pyzbar import pyzbar
import argparse
import cv2

# Build a parameter parser and parse the parameters


# Load input image
image = cv2.imread("mas_qr.jpg")
# Locate the barcode in the image and decode it
barcodes = pyzbar.decode(image)
# Cycle detected barcodes
for barcode in barcodes:
 # The location of the bounding box from which the barcode is extracted
 # Draw the bounding box of the barcode in the image
 (x, y, w, h) = barcode.rect
 cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

 # The barcode data is a byte object, so if we want to print it on the output image
 # To draw it, you need to convert it into a string first
 barcodeData = barcode.data.decode("utf-8")
 barcodeType = barcode.type

 # Draw the barcode data and barcode type on the image
 text = "{} ({})".format(barcodeData, barcodeType)
 cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
  0.5, (0, 0, 255), 2)

 # Print barcode data and barcode type to the terminal
 print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# Show output image
cv2.imshow("Image", image)
cv2.waitKey(0)