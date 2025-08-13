import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, Input, Flatten

train_ds = tf.keras.utils.image_dataset_from_directory(
    directory='food-11/training',
    labels='inferred',
    label_mode='int',
    batch_size=64,
    shuffle=True,
    seed=123
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    directory='food-11/validation',
    labels='inferred',
    label_mode='int',
    batch_size=64,
    shuffle=False,
    seed=123
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    directory='food-11/evaluation',
    labels='inferred',
    label_mode='int',
    batch_size=64,
    shuffle=False,
    seed=123
)

num_classes = len(train_ds.class_names)

resize_and_rescale = tf.keras.Sequential([
    tf.keras.layers.Resizing(64, 64),
    tf.keras.layers.Rescaling(1./255)
])

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomTranslation(0.1, 0.1)
])

train_ds = train_ds.map(lambda x, y: (data_augmentation(resize_and_rescale(x)), y))
val_ds   = val_ds.map(lambda x, y: (resize_and_rescale(x), y))
test_ds  = test_ds.map(lambda x, y: (resize_and_rescale(x), y))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds  = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

model = Sequential([
    Input(shape=(64, 64, 3)),

    Conv2D(64, (3, 3), padding='same', activation="relu"),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation="relu"),
    Dropout(0.3),

    Conv2D(128, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    Conv2D(128, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.5),

    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.5),

    Dense(num_classes, activation="softmax")
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer="adam",
    metrics=['accuracy']
)

model.fit(
    train_ds,
    epochs=20,
    validation_data=val_ds
)

model.save("food_model.h5")

test_loss, test_acc = model.evaluate(test_ds)
print(f"Test accuracy: {test_acc:.2%}")
