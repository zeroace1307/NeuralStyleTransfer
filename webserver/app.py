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
import json
import base64
import tensorflow_hub as hub

USE_TF_HUB = True

def base64string_to_byte(base64string):
    return base64.b64decode(base64string.split(",")[1])

class ImageHandler(tornado.web.RequestHandler):

    def get(self):
        # Get the image data from the request body
        print("hi")

    def post(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        # try:
        # Get the image data from the request body
        # content_byte = self.request.files["content_image"][0].body
        # style_byte = self.request.files["style_image"][0].body

        content_byte = base64string_to_byte(self.get_body_argument("content_image"))
        style_byte = base64string_to_byte(self.get_body_argument("style_image"))

        content_image = load_img_from_byte(content_byte)
        style_image = load_img_from_byte(style_byte)

        if USE_TF_HUB:
            hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
            image_tensor = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
            image_tensor = tf.image.convert_image_dtype(image_tensor[0], dtype=tf.uint8)
        else:
            model = NeuralStyleTransfer(content_image, style_image)

            for _ in range(60):
                model.train_step()

            image_tensor = tf.image.convert_image_dtype(model.output_image[0], dtype=tf.uint8)

        jpeg_bytes = tf.io.encode_jpeg(image_tensor)

        # Send the processed image as a response
        print("Complete!")
        self.set_header("Content-Type", "image/png")
        self.write(jpeg_bytes.numpy())
        # except Exception as e:
        #     error_msg = {'success': True, 'error': str(e)}
        #     print(error_msg)
        #     # self.set_status(e.status_code)
        #     self.write(json.dumps(error_msg))



if __name__ == "__main__":
    app = tornado.web.Application([(r"/image", ImageHandler)])
    app.listen(5001)
    tornado.ioloop.IOLoop.current().start()
