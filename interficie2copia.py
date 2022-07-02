import sys
from PyQt5 import uic
#Cargar nuestro formulario *.ui
formulario = 'interficieQT.ui'
form_class = uic.loadUiType(formulario)[0]
import cv2 as cv
import time
from tempfile import NamedTemporaryFile
from pyzbar import pyzbar
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox)

class captura:
    """ Clase captura, trata con imagenes de una camara de su establecimiento """

    def __init__(self, path):
        self.path = path

    def show(self, frame):
        """ muestra la imagen"""
        return cv.imshow(self, frame)

    def read(self):
        """lee el path de la imagen"""
        return cv.imread(self)

    def detect(self, frame):
        """detecta y localiza codigos QR de una imagen con muchos QRs mediante Inteligencia Artificial y devuelve un array de sus codigos decodificados"""
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
     
        cv.putText(frame, '%.2f s, Qr found: %d' % (elapsed_ms, len(classes)), (240, 340), cv.FONT_HERSHEY_SIMPLEX, 5,
                   COLOR_RED, 20)
        class_names = open('data/obj.names').read().strip().split('\n')
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "%s : %f" % (class_names[classid], score)
            cv.rectangle(frame, box, COLOR_BLUE, 10)
            cv.putText(frame, label, (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_BLUE, 2)
            x, y, w, h = box
            ROI = frame[y:y + h, x:x + w]
            
            print()
            QR.decode(ROI, dictionary, array, frame, x, y)
        cv2.imwrite('image.jpg', frame)
        return array

    net = cv.dnn.readNetFromDarknet('yolov4-tiny-custom-640.cfg', 'backup/yolov4-tiny-custom-640_last.weights')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    model = cv.dnn_DetectionModel(net)

    def procesaI(self):
        """procesa la captura y devuelve una lista de los productos que faltan detectados """

        frame = captura.read(self.path)
        datos = captura.detect(self.path, frame)
        
        print(datos)
        cv2.destroyAllWindows()

        #lista de productos, si lee un QR que no correspone a un producto no lo añade
        products = ["Chorizo", "Fuet", "mini Frankfurts", "Jamon en dulce", "Jamon", "Chistorra", "Butifarra", "Pavo",
                    "Queso", "Sobrassada mallorquina", "Sobrasada"]

        if len(datos) >= 1:
            for i in datos:
                if i not in c and i in products:
                    c.append(i)

                    pass
                else:
                    pass

        return c
class QR:
    """Esta clase trabaja con QR se define con el path de la imagen de un QR"""
    def __init__(self, path):
        self.path = path
    def decode(self, dictionary, array, frame, x_old, y_old):
        """ Decodifica codigos QR proporcionado un diccionario y el array"""
        barcodes = pyzbar.decode(self)
        for barcode in barcodes:
            # The location of the bounding box from which the barcode is extracted
            # Draw the bounding box of the barcode in the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(self, (x, y), (x + w, y + h), (0, 0, 255), 5)

            # The barcode data is a byte object, so if we want to print it on the output image
            # To draw it, you need to convert it into a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # Draw the barcode data and barcode type on the image
            text = "{}".format(barcodeData)
            cv2.putText(frame, text, (x_old , y_old), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 255), 7)
            #se añaden los textos decodificados a un array
            
            array.append(barcodeData)

        return


class VIDEO:
    """ Clase video """
    def __init__(self, path):
        self.path = path
        pass

    def procesaV(self):
        """procesa el video y devuelve una lista de los productos que faltan detectados"""
        ret, frame = self.read()

        try:

            ret, frame = self.read()
            file = NamedTemporaryFile(suffix=".jpg",prefix="./frame_",delete=True)
            cv2.imwrite(file.name, frame)
            ret = captura.detect(file.name, frame)
            captura.show('frame',frame)

            # lista de productos, si lee un QR que no correspone a un producto no lo añade
            products = ["Chorizo", "Fuet", "mini Frankfurts", "Jamon en dulce", "Jamon", "Chistorra","Butifarra","Pavo","Queso","Sobrassada mallorquina","Sobrasada"]

            if len(ret)>=1:
                for i in ret:
                    if i not in c and i in products:
                        c.append(i)

                        pass
                    else:
                        pass


            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

        except Exception as e:
            print(e)

#---------------------------------------------------------------------------
# -------------------------INTERFAZ-----------------------------------------
#---------------------------------------------------------------------------
class Aplicacion(QWidget, form_class):
    """clase aplicacion interficie pyqt5 qt Designer"""

    # Mensaje del boton de ayuda/help de la aplicacion
    MESSAGE = """  EN:\n  This app will detect empty slots from supermarket display racks\n
    IMAGE MODE: select one of the 3 images or file and click IMAGE button to process it\n
    VIDEO MODE: select the recording time and click VIDEO button, camera will open and process live\n
    The detected empty slots will appear in the right side of the screen, as well as an alarm\n
    ESP:\n Esta aplicación detecta cajones vacíos de las estanterías de supermercado\n
    MODO IMAGEN: selecciona una de las 3 imágenes o archivo y clica el botón IMAGE para procesarla\n
    MODO VIDEO : selecciona el tiempo de grabación y clica el botón VIDEO, la cámara se abrira y procesará la grabación \n
    Los cajones vacíos detectados aparecerán a la derecha de la pantalla, una alarma se enciende si hay cajones vacíos\n"""

    # Mensaje de error si se intenta analizar un archivo que no es una imagen (no valido)
    MESSAGES ="""Select image type file"""

    def __init__(self, parent=None):
        import time
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.res = ''
        self.c=[]
        self.not_repeated=[]


    # Implementacion de los Slots referenciados en QDesigner

    def borratodo(self):
        """Eliminar informacion del display y de la lista de cajones vacios (reset)"""
        c.clear()
        self.listWidget.clear()
        self.res = ''
        self.pantalla.setPlainText(self.res)

    def imageinput(self):
        """Seleccionar que imagen analizar"""
        self.listWidget.clear()
        c.clear()
        if self.image1.isChecked():
            input_image = '6vacios.jpg'
            return input_image
        if self.image2.isChecked():
            input_image = '4vacios.jpg'
            return input_image
        if self.image3.isChecked():
            input_image = '0vacios.jpg'
            return input_image
        # Seleccionar una imagen de los archivos del ordenador
        if self.selectfile.isChecked():
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,
                                                      "seleccionar Archivo", '',
                                                      "All Files (*);;Text Files (*.txt)", options=options)
            input_image = fileName
            return input_image


    def image(self):
        """boton de analizar imagen seleccionada"""
        try:
            self.listWidget.clear()
            img = self.imageinput()

            # Executa l'analisi de la imatge

            m = captura(img)
            m.procesaI()

            # Printea el file de la img seleccionada a valor display
            #self.pantalla.setPlainText(str(img))
            self.pantalla.setPlainText('image.jpg')
            new_array = []

            # Pone la imagen del valor en la etiqueta/pantalla de la aplicacion
            im = QPixmap('image.jpg')
            self.label.setPixmap(im)

            # printea el numero de cajones vacios
            self.pantalla_2.setPlainText(str(len(c)))

            # Enciende alarma si hay algo en c (osea detecta algun cajon vacio)
            if len(c)>0:
                # Enciende la alarma
                self.alarm.setStyleSheet("background-color: red;");
            else:

                # Apaga alarma
                self.alarm.setStyleSheet("background-color: white;");


            # Añadir a la lista de la derecha de la pantalla lo que haya en c,(osea los productos detectados)
            for string in c:
                self.listWidget.insertItem(0, string)
            self.res = ''
        except Exception as e:
            # Excepcion por si se intenta analizar un archivo que no es imagen, saltara un mensaje de error
            QMessageBox.information(self, 'Help', self.MESSAGES)
            print(e)
    def video(self):
        """boton de analizar video"""
        # Borra la lista anterior de productos detectados para actualizarla
        c.clear()
        self.listWidget.clear()
        # Poner en el display de informacion que se ha capturado el video
        self.pantalla.setPlainText(str("captura de video"))
        self.label.clear()

        im = QPixmap('fondograbacon.png')
        self.label.setPixmap(im)

        value = self.min.value()
        timeout = time.time() + value   # 20 seconds
        not_repeated = []
        while True:
            if time.time()<timeout:
                ret = VIDEO.procesaV(cv2.VideoCapture(0))
                for string in c:
                    if string not in not_repeated:
                        self.listWidget.insertItem(0, string)
                        not_repeated.append(string)
                self.res = ''
            else:
                cv2.destroyAllWindows()
                break
    def help(self):
        """Muestra el mensaje de ayuda de la aplicacion"""
        QMessageBox.information(self,'Help',self.MESSAGE)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyWindow = Aplicacion(None)
    MyWindow.show()

    c = []

    app.exec_()

