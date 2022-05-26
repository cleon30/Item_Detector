
from operator import truediv
import cv2 as cv
import numpy as np
import time
import tempfile #ha canviat aixo posant a tot arreu on surt tempfile.etc
from pandas import array
from pyzbar import pyzbar
import argparse
import cv2



class qr_detector:
    """ crec que hauriem de posarli IMAGE o CPTURA de nombre i totes les def han de tenir noms mes clars i sempre utilitzar self """

    # crec que hauriem de tenir una classe IMAGE o CAPTURA on fem tot el que NO sigui treballar amb QR sols sino amb
    # la captura dels supers i despres una classe a part que es digui QR que tingui la funció decode que decodifica els QR

    def __init__(self, path):
        self.path = path

    def show(self, frame):
        """ muestra el QR"""
        return cv.imshow(self, frame)

    def read(self):
        """lee el path del QR"""
        return cv.imread(self)

    def decoder(image, dictionary, array):
        """ decodifica codigos QR """
        barcodes = pyzbar.decode(image)
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

            array.append(barcodeData)

        return

        # Show output image

    def detect(self, frame):
        """detecta codigos QR  de una imagen con muchos QRs y devuelve un array de sus codigos decodificados"""
        width = 640
        height = 640
        if frame.shape[1] > 1024 or frame.shape[0] > 1024:
            width = 1024
            height = 1024
            qr_detector.model.setInputParams(size=(width, height), scale=1 / 255, swapRB=True)

        # Inferencing
        CONFIDENCE_THRESHOLD = 0.2
        NMS_THRESHOLD = 0.4
        COLOR_RED = (0, 0, 255)
        COLOR_BLUE = (255, 0, 0)
        start_time = time.time()
        classes, scores, boxes = qr_detector.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
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
            qr_detector.decoder(ROI, dictionary, array)
            # file.close()
        # qr_detector.show(self, frame)
        return array

    net = cv.dnn.readNetFromDarknet('yolov4-tiny-custom-640.cfg', 'backup/yolov4-tiny-custom-640_last.weights')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    model = cv.dnn_DetectionModel(net)

    # frame = cv.imread('test03.jpg')
    # detect('test03.jpg', frame)


class Mode:
    """  """

    def __init__(self, path):
        """
        >>>
        """
        self.path = path

    def Video(self):
        ret, frame = self.path.read()
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", prefix="./frame_", delete=True) as file:
                cv2.imwrite(file.name, frame)
                ret = qr_detector.detect(file.name, frame)
                qr_detector.show('frame', frame)
                if len(ret) >= 1:
                    for i in ret:
                        if i not in c:
                            c.append(i)
                        else:
                            pass
                print(c)
                # print(ret)
        except Exception as e:
            print(e)
        return c

    def IP_Camera(self):
        frame = qr_detector.read(self.path)
        datos = qr_detector.detect(self.path, frame)
        print(datos)
        cv2.destroyAllWindows()
        return datos


if __name__ == '__main__':
    m = Mode('mejor_captura10.png')
    print(m.IP_Camera())
    exit()

    video = True
    input_video = cv2.VideoCapture(0)
    input_imatge = 'mejor_captura10.png'
    new_array = []
    if video == True:
        c = []
        Mode.Video(input_video)

    else:
        Mode.IP_Camera(input_imatge)
