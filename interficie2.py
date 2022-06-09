import sys
from PyQt5 import uic
# Cargar nuestro formulario *.ui
formulario = 'interficieQT.ui'
form_class = uic.loadUiType(formulario)[0]
#from this import d
from operator import truediv
import cv2 as cv
import numpy as np
import time
from tempfile import NamedTemporaryFile
from pandas import array
from pyzbar import pyzbar
import argparse
import cv2
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys


# He creat una classe IMAGE o CAPTURA on fem tot el que NO sigui treballar amb QR sols sino amb
# la captura dels supers i despres una classe a part que es digui QR que tingui la funció decode que decodifica els QR
# esta afegit el main on ha d'estar el programa principal
#he borrat el tempfiles aparentment innecesari per a la def detect


class captura:
    """ crec que hauriem de posarli IMAGE o CPTURA de nombre i totes les def han de tenir noms mes clars i sempre utilitzar self """


    def __init__(self, path):
        self.path = path

    def show(self, frame):
        """ muestra el QR"""
        return cv.imshow(self, frame)

    def read(self):
        """lee el path del QR"""
        return cv.imread(self)

    def detect(self, frame):
        """detecta codigos QR  de una imagen con muchos QRs y devuelve un array de sus codigos decodificados"""
        width = 640
        height = 640
        if frame.shape[1] > 1024 or frame.shape[0] > 1024:
            width = 1024
            height = 1024
            captura.model.setInputParams(size=(width, height), scale=1 / 255, swapRB=True)

        # Inferencing
        CONFIDENCE_THRESHOLD = 0.2
        NMS_THRESHOLD = 0.4
        COLOR_RED = (0, 0, 255)
        COLOR_BLUE = (255, 0, 0)
        start_time = time.time()
        classes, scores, boxes = captura.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        elapsed_ms = time.time() - start_time
        dictionary = {}
        array = []
        cv.putText(frame, '%.2f s, Qr found: %d' % (elapsed_ms, len(classes)), (40, 40), cv.FONT_HERSHEY_SIMPLEX, 1,
                   COLOR_RED, 2)
        class_names = open('data/obj.names').read().strip().split('\n')
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "%s : %f" % (class_names[classid], score)
            cv.rectangle(frame, box, COLOR_BLUE, 2)
            # cv.putText(frame, label, (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_BLUE, 2)
            x, y, w, h = box
            ROI = frame[y:y + h, x:x + w]
            print()
            #se ha borrado la creación de archivos temporales porque al parecer
            # file = tempfile.NamedTemporaryFile(suffix=".jpg",prefix="./frame_",delete=True)
            # cv.imwrite(file.name, ROI)
            QR.decode(ROI, dictionary, array)
            # file.close()
        # qr_detector.show(self, frame)
        return array

    net = cv.dnn.readNetFromDarknet('yolov4-tiny-custom-640.cfg', 'backup/yolov4-tiny-custom-640_last.weights')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    model = cv.dnn_DetectionModel(net)

    # frame = cv.imread('test03.jpg')
    # detect('test03.jpg', frame)
    def IP_Camera(self):
        """procesa la captura y devuelve una lista de los productos detectados """

        frame = captura.read(self.path)
        datos = captura.detect(self.path, frame)
        print(datos)
        cv2.destroyAllWindows()
        if len(datos) >= 1:
            for i in datos:
                if i not in c:
                    c.append(i)

                    pass
                else:
                    pass

        return c
class QR:
    """Esta clase trabaja con QR se define con el path de la imagen de un QR"""
    def __init__(self, path):
        self.path = path
    def decode(self, dictionary, array):
        """ Decodifica codigos QR proporcionado un diccionario(creo que lo del diccionario de momento no se usa o el array?) y el array"""
        #he canviat image per self y el nom de la funcio de decode a decoder
        barcodes = pyzbar.decode(self)
        for barcode in barcodes:
            # The location of the bounding box from which the barcode is extracted
            # Draw the bounding box of the barcode in the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(self, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # The barcode data is a byte object, so if we want to print it on the output image
            # To draw it, you need to convert it into a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # Draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(self, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)

            array.append(barcodeData)

        return

        # Show output image
#NO tinc molt clar si podriem definir una classe nomes pel video que es digui VIDEO i la funcio processadoV
#Li he canviat els noms ja, pero s'ha d'arreglar perque funcioni que aixo ho saps millor tu.( s'ha de deixar lo de try with)
class VIDEO:
    """ Clase video """
#clase antes MODO -> ahora VIDEO
    def __init__(self, path):
        """
       # >>>
        """
        pass

    def procesadoV(self):
        """def antes video -> ahora procesadoV"""
        ret, frame = self.read()
        #la escritura se tiene que hacer con esta estructura de try y with, s'ha de repassar i mirar que no ho haguem de fer en un altre lloc
        try:
            
            ret, frame = self.read()
            file = NamedTemporaryFile(suffix=".jpg",prefix="./frame_",delete=True)
            cv2.imwrite(file.name, frame)
            ret = captura.detect(file.name, frame)
            captura.show('frame',frame)
            if len(ret)>=1:
                for i in ret:
                    if i not in c:
                        c.append(i)
                        
                        pass
                    else:
                        pass

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

        except Exception as e:
            print(e)


# ----------INTERFAZ-----------------------
class MiCalculadora(QWidget, form_class):
    def __init__(self, parent=None):
        import time
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.res = ''
        self.c=[]
        self.not_repeated=[]
        
       
    # Implementacion de los Slots referenciados en QDesigner

    def borratodo(self):
        c.clear()
        self.listWidget.clear()
        self.res = ''
        self.pantalla.setPlainText(self.res)
  
    def imageinput(self):
        self.listWidget.clear()
        c.clear()
        if self.image1.isChecked():
            input_image = 'mejor_captura10.png'
            return input_image
        if self.image2.isChecked():
            input_image = 'mejor_captura10.png'
            return input_image
        if self.image3.isChecked():
            input_image = 'QRcomida.jpg'
            return input_image

    def image(self):

        self.listWidget.clear()
        valor = self.imageinput()
        self.pantalla.setPlainText(str(valor))
        #printea el file de la img seleccionada a valor

        new_array = []
        #self.label.pixmap(valor)

        m = captura(self.imageinput())
        m.IP_Camera()
        #c=['Chorizo', 'Fuet', 'Jamon', 'Queso', 'Butifarra']
        for string in c:
            self.listWidget.insertItem(0, string)
        self.res = ''

    def evalua(self):
        c.clear()
        self.listWidget.clear()
        value = self.min.value()
        timeout = time.time() + value   # 20 seconds
        not_repeated = []
        while True:
            if time.time()<timeout:
                ret = VIDEO.procesadoV(cv2.VideoCapture(0))
                for string in c:
                    if string not in not_repeated:
                        self.listWidget.insertItem(0, string)
                        not_repeated.append(string)
                self.res = ''
            else:
                cv2.destroyAllWindows()
                break
    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyWindow = MiCalculadora(None)
    MyWindow.show()
    #---
    c = []

    #---
    app.exec_()
    #exit()