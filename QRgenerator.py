
import pyqrcode
import png
def create_qr(data):
    url = pyqrcode.create(str(data))
    url.png('myqr.png', scale = 10)
