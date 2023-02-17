"""
NeuralStyleTransfer Model Script
"""

import tensorflow as tf


def gram_matrix(input_tensor):
    """
    Compute gram matrix

    Args:
        input_tensor: tensor

    Returns:
        gram matrix
    """
    result = tf.linalg.einsum("bijc,bijd->bcd", input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / num_locations


def vgg_layers(layer_names):
    """
    Creates a VGG model that returns a list of intermediate output values.

    Args:
        layer_names: name of the layers

    Returns:
        vgg layer
    """
    # Load our model. Load pretrained VGG, trained on ImageNet data
    vgg = tf.keras.applications.VGG19(include_top=False, weights="imagenet")
    vgg.trainable = False

    outputs = [vgg.get_layer(name).output for name in layer_names]

    model = tf.keras.Model([vgg.input], outputs)
    return model


def clip_0_1(image):
    """
    Clip between 0 and 1

    Args:
        image: image

    Returns:
        image with clipped value
    """
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


class NeuralStyleTransfer(tf.keras.models.Model):
    """
    NeuralStyleTransfer Model
    """

    def __init__(self, content_image: tf.Tensor, style_image: tf.Tensor):
        """
        Initialise neural style transfer model

        Args:
            content_image: content image in pillow format
            style_image:  style image in pillow format
        """
        super().__init__()
        self.content_layers = ["block5_conv2"]
        self.style_layers = [
            "block1_conv1",
            "block2_conv1",
            "block3_conv1",
            "block4_conv1",
            "block5_conv1",
        ]
        self.vgg = vgg_layers(self.style_layers + self.content_layers)
        self.num_style_layers = len(self.style_layers)
        self.num_content_layers = len(self.content_layers)
        self.vgg.trainable = False

        self.style_targets = self.set_style_targets(style_image)
        self.content_targets = self.set_content_targets(content_image)
        self.style_weight = 1e-2
        self.content_weight = 1e4

        self.opt = tf.keras.optimizers.Adam(
            learning_rate=0.02, beta_1=0.99, epsilon=1e-1
        )
        self.content_image = content_image
        self.style_image = style_image
        self.output_image = tf.Variable(content_image)

    def set_style_targets(self, style_image: tf.Tensor) -> tf.Tensor:
        """
        Set style target

        Args:
            style_image:  style image

        Returns:
            style target
        """
        return self.extract_features(style_image)["style"]

    def set_content_targets(self, content_image: tf.Tensor) -> tf.Tensor:
        """
        Set content target

        Args:
            content_image: content image

        Returns:
            content target
        """
        return self.extract_features(content_image)["content"]

    def get_model_output(self):
        """
        Get model output

        Returns:
            model output image
        """
        return self.output_image

    def extract_features(self, inputs):
        """
        Extract features of the image

        Args:
            inputs: input images

        Returns:
            features of the image in tensor format
        """
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (
            outputs[: self.num_style_layers],
            outputs[self.num_style_layers :],
        )

        style_outputs = [gram_matrix(style_output) for style_output in style_outputs]

        content_dict = dict(zip(self.content_layers, content_outputs))

        style_dict = dict(zip(self.style_layers, style_outputs))

        return {"content": content_dict, "style": style_dict}

    @tf.function()
    def train_step(self):
        """
        Training step
        """
        with tf.GradientTape() as tape:
            outputs = self.extract_features(self.output_image)
            loss = self.style_content_loss(outputs)

        grad = tape.gradient(loss, self.output_image)
        self.opt.apply_gradients([(grad, self.output_image)])
        self.output_image.assign(clip_0_1(self.output_image))

    def style_content_loss(self, outputs):
        """
        Loss function

        Args:
            outputs: output image

        Returns:
            compute loss
        """
        style_outputs = outputs["style"]
        content_outputs = outputs["content"]
        style_loss = tf.add_n(
            [
                tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                for name in style_outputs.keys()
            ]
        )
        style_loss *= self.style_weight / self.num_style_layers

        content_loss = tf.add_n(
            [
                tf.reduce_mean(
                    (content_outputs[name] - self.content_targets[name]) ** 2
                )
                for name in content_outputs.keys()
            ]
        )
        content_loss *= self.content_weight / self.num_content_layers
        loss = style_loss + content_loss
        return loss
