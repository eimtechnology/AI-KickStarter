'''
Don't forget to install cv2-python via pip.
Keras will be installed automatically when installing cv2-python.

The training set could be downloaded from this link:
https://eimtechnology.blob.core.windows.net/dataset/dataset.zip
'''
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

# Data Preprocessing
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# Load training and validation sets
training_set = train_datagen.flow_from_directory(
    './dataset/training_set',
    target_size=(50, 50),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_set = train_datagen.flow_from_directory(
    './dataset/training_set',
    target_size=(50, 50),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# Build CNN Model
model = Sequential()

# Add more convolutional layers with increasing filters
model.add(Conv2D(64, (3, 3), input_shape=(50, 50, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))  # Add dropout to reduce overfitting

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))

# Flattening
model.add(Flatten())

# Fully Connected Layers
model.add(Dense(units=256, activation='relu'))
model.add(Dropout(0.5))  # Increase dropout to prevent overfitting
model.add(Dense(units=1, activation='sigmoid'))  # Binary output

# Compile the model with lower learning rate for more precision
optimizer = Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Model Summary
model.summary()

# Callbacks: Early Stopping and Model Checkpoint
early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1, restore_best_weights=True)
checkpoint = ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True, verbose=1)

# Train the model with validation set
history = model.fit(
    training_set,
    epochs=10,
    validation_data=validation_set,
    callbacks=[early_stop, checkpoint]
)

# Evaluate on the validation set
val_loss, val_accuracy = model.evaluate(validation_set)
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

# Test Data Preprocessing
test_set = train_datagen.flow_from_directory(
    './dataset/test_set',
    target_size=(50, 50),
    batch_size=32,
    class_mode='binary'
)

# Evaluate on the test data
test_loss, test_accuracy = model.evaluate(test_set)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Function for Predicting a Single Image
def predict_single_image(model, image_path):
    img = load_img(image_path, target_size=(50, 50))
    img_array = img_to_array(img) / 255.0
    img_array = img_array.reshape(1, 50, 50, 3)
    result = (model.predict(img_array) > 0.5).astype("int32")
    label = 'Dog' if result[0][0] == 1 else 'Cat'
    return label

# Predict Single Images (Dog and Cat)
print("Dog Image Prediction:", predict_single_image(model, 'dog.jpg'))
print("Cat Image Prediction:", predict_single_image(model, 'cat1.jpg'))

# Batch Prediction and Visualization for Multiple Images
def predict_and_display_images(model, image_files):
    fig = plt.figure(figsize=(10, 10))
    for i, img_name in enumerate(image_files):
        img_ori = load_img(img_name, target_size=(50, 50))
        img_array = img_to_array(img_ori) / 255.0
        img_array = img_array.reshape(1, 50, 50, 3)
        
        result = (model.predict(img_array) > 0.5).astype("int32")
        label = 'dog' if result[0][0] == 1 else 'cat'
        
        img_display = load_img(img_name, target_size=(250, 250))
        plt.subplot(3, 3, i+1)
        plt.imshow(img_display)
        plt.title(f'predict: {label}')
        
    plt.show()

# Predict and display images 1.jpg to 9.jpg
image_files = [f"{i}.jpg" for i in range(1, 9)]
predict_and_display_images(model, image_files)
