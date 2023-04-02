# -*- coding: utf-8 -*-
"""malaria_cell.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MyDY4eGO7L_zqgbTbjYQj2iOctE2cLBL
"""

import numpy as np
np.random.seed(1000)
import cv2
import os
from PIL import Image
import keras

img_dir="C:/Users/Asus/Downloads/cell_images"
dataset=[]
label=[]

parasitized_img=os.listdir("C:/Users/Asus/Downloads/cell_images/Parasitized")
for i , image_name in enumerate(parasitized_img):
  if (image_name.split('.')[1]=='png'):
    image=cv2.imread("C:/Users/Asus/Downloads/cell_images/Parasitized"+image_name)
    image=Image.fromarray(image,'RGB')
    image=image.resize((64,64))
    dataset.append(np.array(image))
    label.append(0)

    uninfected_img=os.listdir("C:/Users/Asus/Downloads/cell_images/Uninfected")
for i , image_name in enumerate(uninfected_img):
  if (image_name.split('.')[1]=='png'):
    image=cv2.imread("C:/Users/Asus/Downloads/cell_images/uninfected"+image_name)
    image=Image.fromarray(image,'RGB')
    image=image.resize((64,64))
    dataset.append(np.array(image))
    label.append(1)

Input_Shape=(64,64,3)

input=keras.layers.Input(shape=Input_Shape)

conv1=keras.layers.Conv2D(32,(3,3),activation="relu",padding="same")(input)

pool1=keras.layers.MaxPooling2D((2,2))(conv1)
norm1=keras.layers.BatchNormalization(axis=-1)(pool1)
drop1=keras.layers.Dropout(0.2)(norm1)

conv2=keras.layers.Conv2D(32,(3,3),activation="relu",padding="same")(drop1)

pool2=keras.layers.MaxPooling2D((2,2))(conv2)
norm2=keras.layers.BatchNormalization(axis=-1)(pool2)
drop2=keras.layers.Dropout(0.2)(norm2)

flat=keras.layers.Flatten()(drop2)

hid1=keras.layers.Dense(512,activation="relu")(flat)

norm3=keras.layers.BatchNormalization(axis=-1)(hid1)
drop3=keras.layers.Dropout(0.2)(norm3)

hid2=keras.layers.Dense(256,activation="relu")(drop3)
 
norm4=keras.layers.BatchNormalization(axis=-1)(hid2)
drop4=keras.layers.Dropout(0.2)(norm4)           

out=keras.layers.Dense(2,activation="sigmoid")(drop4)

model=keras.Model(inputs=input,outputs=out)
model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])

print(model.summary())

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

X_train, X_test, y_train, y_test = train_test_split(dataset, to_categorical(np.array(label)), test_size = 0.20, random_state = 0)

history = model.fit(np.array(X_train), 
                         y_train, 
                         batch_size = 64, 
                         verbose = 1, 
                         epochs = 5,      #Changed to 3 from 50 for testing purposes.
                         validation_split = 0.1,
                         shuffle = False
                      
                     )

print("Test_Accuracy: {:.2f}%".format(model.evaluate(np.array(X_test), np.array(y_test))[1]*100))

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
t = f.suptitle('CNN Performance', fontsize=12)
f.subplots_adjust(top=0.85, wspace=0.3)

max_epoch = len(history.history['accuracy'])+1
epoch_list = list(range(1,max_epoch))
ax1.plot(epoch_list, history.history['accuracy'], label='Train Accuracy')
ax1.plot(epoch_list, history.history['val_accuracy'], label='Validation Accuracy')
ax1.set_xticks(np.arange(1, max_epoch, 5))
ax1.set_ylabel('Accuracy Value')
ax1.set_xlabel('Epoch')
ax1.set_title('Accuracy')
l1 = ax1.legend(loc="best")

ax2.plot(epoch_list, history.history['loss'], label='Train Loss')
ax2.plot(epoch_list, history.history['val_loss'], label='Validation Loss')
ax2.set_xticks(np.arange(1, max_epoch, 5))
ax2.set_ylabel('Loss Value')
ax2.set_xlabel('Epoch')
ax2.set_title('Loss')
l2 = ax2.legend(loc="best")

model.save('malaria_cnn.h5')