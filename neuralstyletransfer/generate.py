from neuralstyletransfer.model import NeuralStyleTransfer
from neuralstyletransfer.utils import imshow, load_img, tensor_to_image, load_img_from_byte
import matplotlib.pyplot as plt

style_path = "image_examples/kandinsky5.jpg"
content_path = "image_examples/YellowLabradorLooking_new.jpg"


def generate_image

content_image = load_img_from_byte(content_byte)
style_image = load_img_from_byte(style_byte)


# plt.subplot(1, 2, 1)
# imshow(content_image, "Content Image")
#
# plt.subplot(1, 2, 2)
# imshow(style_image, "Style Image")

model = NeuralStyleTransfer(style_image, content_image)
model.train_step()
model.train_step()
model.train_step()
model.train_step()

tensor_to_image(model.output_image)