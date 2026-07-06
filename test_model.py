import tensorflow as tf

print("TensorFlow:", tf.__version__)

try:
    model = tf.keras.models.load_model("models/alzhemers.h5", compile=False)
    print("Model loaded successfully!")
    model.summary()
except Exception as e:
    print(type(e).__name__)
    print(e)