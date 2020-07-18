import numpy as np
import chords_imp
from sklearn.model_selection import train_test_split
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import data_set

def model_train(X_train,y_train):
    checkpoint_path = "wts/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    inputs = keras.Input(shape=(12,))
    dense = layers.Dense(1000, activation="relu")
    x = dense(inputs)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(35, activation="relu")(x)
    outputs = layers.Dense(len(chords_imp.chords))(x)
    model = keras.Model(inputs=inputs, outputs=outputs)

    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),optimizer=keras.optimizers.SGD(learning_rate=0.01, momentum=0.95),metrics=["accuracy"],)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,save_weights_only=True,verbose=1)
    history = model.fit(X_train, y_train, batch_size=300, epochs=1000, validation_split=0.2,callbacks=[cp_callback])
    test_scores = model.evaluate(data_set.X_test, data_set.y_test, verbose=2)
    print("Test loss:", test_scores[0])
    print("Test accuracy:", test_scores[1])

model_train(data_set.X_train,data_set.y_train)
