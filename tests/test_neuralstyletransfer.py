from neuralstyletransfer.model import NeuralStyleTransfer
from neuralstyletransfer.utils import load_img
from pathlib import Path
import os


class TestNeuralStyleTransfer:
    def test_e2e_pipeline(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        style_path = "{}/image_examples/kandinsky5.jpg".format(current_dir)
        content_path = "{}/image_examples/YellowLabradorLooking_new.jpg".format(
            current_dir
        )

        content_image = load_img(content_path)
        style_image = load_img(style_path)

        model = NeuralStyleTransfer(style_image, content_image)
        model.train_step()
        model.train_step()
