# Detector de Stock 

### **馃懢馃懢馃懢 Bienvenido 馃懢馃懢馃懢**
### **Introducci贸n**

Este proyecto tiene como objetivo poder facilitar la detecci贸n de falta de stock en supermercados o tiendas, mediante la adici贸n de codigos QR debajo de los productos, de modo que cuando hay falta de material, el propio QR queda al descubierto y la camara puede analizar este QR y saber que producto falta. 

Existen dos modos de uso en nuestra aplicaci贸n, el primero es mediante imagenes y el segundo es mediante video. En ambos modos, los frames son analizados mediante un modelo preentrenado de Deep Learning especializado en detecci贸n de codigos QR, haciendo que se detecten con facilidad y puedan ser procesados a una libreria de escaneo de codigos QR y asi obtener el producto correspondiente.


Para inicializar el proyecto, clona este repositorio y sigue las instrucciones que hay a continuaci贸n.
## Instalaci贸n de Librerias :
```bash
pip3 install opencv-python
pip3 install pyzbar
pip3 install PyQt5
pip3 install tempfile
```
## Instalaci贸n de aplicaci贸n en dispositivo Movil
Probablemente esta sea la parte m谩s complicada del set up, pero basicamente debes instalar una aplicaci贸n de terceros 
para comunicar el Movil con el Ordenador. En nuestro caso hemos utilizado MacOS con iOS a trav茅s de la aplicaci贸n EpocCam Pro.
    
## Ejecuci贸n del programa Python3 
    
Simplemente debes introducir la instrucci贸n `python3 Detector_Stock.py`en la terminal

Sientete libre de realizar fork o mejorar el proyecto actual :) 



<img width="1295" alt="Captura de Pantalla 2022-07-02 a las 4 44 27" src="https://user-images.githubusercontent.com/62452212/176983835-da43187d-02b1-4d92-a565-43c82f5e87b2.png">


Proyecto realizado por Sergi Saperas y Carlos Martin 
