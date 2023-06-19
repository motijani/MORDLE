import tensorflow as tf
from tensorflow import keras

model = tf.keras.Sequential([
    tf.keras.layers.GRU(32, input_shape=(None, 1)),  # GRU layer with 32 units
    tf.keras.layers.Dense(1)  # Output layer
])