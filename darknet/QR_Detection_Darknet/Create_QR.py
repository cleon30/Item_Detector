# importing the qrcode library  
import qrcode  
# generating a QR code using the make() function  
qr_img = qrcode.make("1")  
# saving the image file  
qr_img.save("qr-img.jpg")  