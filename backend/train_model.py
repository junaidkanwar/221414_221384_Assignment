import tensorflow as tf
import numpy as np
from datasets import load_dataset
from PIL import Image

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5

dataset = load_dataset("Bingsu/Human_Action_Recognition")

class_names = dataset["train"].features["labels"].names
num_classes = len(class_names)

def preprocess(example):
    image = example["image"]
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    image = image.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image, dtype=np.float32) / 255.0
    label = example["labels"]
    return image, label

def dataset_generator(hf_dataset):
    """Generator function to yield images one at a time"""
    for i in range(len(hf_dataset)):
        item = hf_dataset[i]
        img, lbl = preprocess(item)
        yield img, lbl

def to_tf_dataset(hf_dataset):
    """Convert HuggingFace dataset to TensorFlow dataset using generator"""
    return tf.data.Dataset.from_generator(
        lambda: dataset_generator(hf_dataset),
        output_signature=(
            tf.TensorSpec(shape=(IMG_SIZE, IMG_SIZE, 3), dtype=tf.float32),
            tf.TensorSpec(shape=(), dtype=tf.int64)
        )
    ).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

train_ds = to_tf_dataset(dataset["train"])
test_ds = to_tf_dataset(dataset["test"])

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS)

model.save("action_model.h5")

print("Model training completed and saved.")
