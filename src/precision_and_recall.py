from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
import numpy as np
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import load_model

# Load data set
test_ds = tf.keras.utils.image_dataset_from_directory(
    directory='../data/testing',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    shuffle=False,
    seed=123
)

# Normalize and resize data
resize_and_rescale = tf.keras.Sequential([
  tf.keras.layers.Resizing(32, 32),
  tf.keras.layers.Rescaling(1./255)
])
test_ds = test_ds.map(lambda x, y: (resize_and_rescale(x), y))

# Extract images and labels as NumPy arrays
y_true = np.concatenate([y.numpy() for _, y in test_ds], axis=0)

# Load trained model
model = load_model('food_model.h5')

# Get predictions
y_pred_probs = model.predict(test_ds, verbose=1)

# For binary classification:
y_pred = (y_pred_probs > 0.5).astype(int).flatten()

# Metrics
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f"True Positives: {tp}")
print(f"True Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

print("\nClassification Report:")
print(classification_report(y_true, y_pred))