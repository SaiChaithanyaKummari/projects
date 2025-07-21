import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

def load_and_preprocess_data():
    # Load the MNIST dataset
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    
    train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255
    
    train_labels = keras.utils.to_categorical(train_labels)
    test_labels = keras.utils.to_categorical(test_labels)
    
    return train_images, train_labels, test_images, test_labels

def create_model():
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        
        layers.Flatten(),
        
      
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  
    ])
    
    return model

def train_model(model, train_images, train_labels, test_images, test_labels):
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    history = model.fit(train_images, train_labels,
                        epochs=10,
                        batch_size=64,
                        validation_data=(test_images, test_labels))
    
    return history

def evaluate_model(model, test_images, test_labels):
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f'Test accuracy: {test_acc:.4f}')
    return test_loss, test_acc

def plot_history(history):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    train_images, train_labels, test_images, test_labels = load_and_preprocess_data()
    
    model = create_model()
    model.summary()  
    
    history = train_model(model, train_images, train_labels, test_images, test_labels)
    
    evaluate_model(model, test_images, test_labels)
    
    plot_history(history)
    
    model.save('mnist_cnn.h5')
    print("Model saved as mnist_cnn.h5")

if __name__ == "__main__":
    main()