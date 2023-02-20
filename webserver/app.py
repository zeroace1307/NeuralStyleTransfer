import io
import tornado.ioloop
import tornado.web
import numpy as np
import cv2
from neuralstyletransfer.utils import load_img_from_byte
from neuralstyletransfer.model import NeuralStyleTransfer
from neuralstyletransfer.utils import imshow, load_img, tensor_to_image
import matplotlib.pyplot as plt
import tensorflow as tf
class ImageHandler(tornado.web.RequestHandler):

    def get(self):
        # Get the image data from the request body
        print("hi")

    def post(self):
        # Get the image data from the request body
        content_byte = self.request.files["content_image"][0].body
        style_byte = self.request.files["style_image"][0].body

        content_image = load_img_from_byte(content_byte)
        style_image = load_img_from_byte(style_byte)

        model = NeuralStyleTransfer(content_image, style_image)

        for _ in range(60):
            model.train_step()

        image_tensor = tf.image.convert_image_dtype(model.output_image[0], dtype=tf.uint8)
        jpeg_bytes = tf.io.encode_jpeg(image_tensor)

        # Send the processed image as a response
        self.set_header("Content-Type", "image/png")
        self.write(jpeg_bytes.numpy())


if __name__ == "__main__":
    app = tornado.web.Application([(r"/image", ImageHandler)])
    app.listen(5001)
    tornado.ioloop.IOLoop.current().start()
