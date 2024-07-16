import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
def classify():
    # Load VGG16 model pretrained on ImageNet
    model = VGG16(weights='imagenet')
    
    # Load and preprocess image
    img_path = 'temp/stored_picture.png'
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # Predict image class
    preds = model.predict(x)
    decoded_preds = decode_predictions(preds, top=1)[0]  # Top 3 predictions
    first_prediction = decoded_preds[0] if decoded_preds else ('Unknown', 0.0)
    label = first_prediction[1]
    return label

# Example usage:
