__author__ = 'qibai'
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.optimizers import SGD
from keras import backend as K
from keras.utils import np_utils
import os
import cv2
import numpy as np


def get_images(image_dir, label_file):
    # image_dir = "/home/qibai/Documents/smpData/images/"
    # dirname = "../images/"

    images = {}
    labels = {}
    age = 2
    gender = 1
    area = 3
    # label_file = open("../data-normalized/label_maps.csv")
    for line in label_file:
        items = line.strip().split(",")
        if items[gender] != "":
            labels[items[0]] = items[gender]
    for parent, dirnames, filenames in os.walk(image_dir):
        for filename in filenames:
            if filename not in labels:
                print ("can't find user :" + filename)
                continue
            images[filename] = os.path.join(parent, filename)

    X_train = np.zeros((len(images), 180, 180, 3), dtype="uint8")
    y_train = np.zeros((len(images),), dtype="uint8")

    i = 0
    for key in images:
        try:
            X_train[i, :, :, :] = cv2.imread(images.get(key))
            y_train[i] = labels.get(key)
            i += 1
        except:
            print (key)
    return (X_train, y_train)


def load_data():
    train_dirname = "../images/"
    # train_dirname = "/home/qibai/Documents/smpData/images/"
    train_label = open("../data-normalized/label_maps.csv")
    vali_dirname = "../test_images/"
    # vali_dirname = "/home/qibai/Documents/smpData/test_images/"
    vali_label = open("../data-normalized/validation.txt")

    return get_images(train_dirname, train_label), get_images(vali_dirname, vali_label)


batch_size = 32
nb_classes = 2
first_epoch = 60
second_epoch = 100
data_augmentation = False

# input image dimensions
img_rows, img_cols = 180, 180
# the CIFAR10 images are RGB
img_channels = 3

# the data, shuffled and split between train and test sets
# (X_train, y_train), (X_test, y_test) = cifar10.load_data()
(X_train, y_train), (X_vali, y_vali) = load_data()
print('X_train shape:', X_train.shape)
print('X_vali shape:', X_vali.shape)
print(X_train.shape[0], 'train samples')
print(X_vali.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_vali = np_utils.to_categorical(y_vali, nb_classes)

# create the base pre-trained model
K.set_image_dim_ordering("tf")
base_model = VGG16(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3, name="drp1")(x)
# x = Flatten(name='flatten', input_shape=(img_rows, img_cols, img_channels))(x)
x = Dense(100, activation='relu', name='fc1')(x)
x = Dropout(0.3, name="drp2")(x)
x = Dense(100, activation='relu', name='fc2')(x)
predictions = Dense(nb_classes, activation='softmax', name='predictions')(x)
# x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
# x = Dense(100, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
# predictions = Dense(2, activation='softmax')(x)

# this is the model we will train
model = Model(input=base_model.input, output=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
# sgd = SGD(lr=0.02, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])

# train the model on the new data for a few epochs
# model.fit_generator(...)
# model.fit(X_train, Y_train,
#           batch_size=batch_size,
#           nb_epoch=nb_epoch,
#           # validation_data=(X_test, Y_test),
#           validation_split=0.2,
#           shuffle=True)
# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(model.layers):
    print(i, layer.name)
print('Using real-time data augmentation.')

# this will do preprocessing and realtime data augmentation
datagen = ImageDataGenerator(
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
    width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
    horizontal_flip=True,  # randomly flip images
    vertical_flip=False)  # randomly flip images

# compute quantities required for featurewise normalization
# (std, mean, and principal components if ZCA whitening is applied)
datagen.fit(X_train)

# fit the model on the batches generated by datagen.flow()
model.fit_generator(datagen.flow(X_train, Y_train,
                                 batch_size=batch_size),
                    samples_per_epoch=X_train.shape[0],
                    nb_epoch=first_epoch,
                    validation_data=(X_vali, Y_vali))
# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 172 layers and unfreeze the rest:
# for layer in model.layers[:15]:
#    layer.trainable = False
# for layer in model.layers[15:]:
#    layer.trainable = True
#
# # we need to recompile the model for these modifications to take effect
# # we use SGD with a low learning rate
# from keras.optimizers import SGD
# model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
#
# # we train our model again (this time fine-tuning the top 2 inception blocks
# # alongside the top Dense layers
# # model.fit_generator(...)
# model.fit_generator(datagen.flow(X_train, Y_train,
#                                  batch_size=batch_size),
#                     samples_per_epoch=X_train.shape[0],
#                     nb_epoch=30,
#                     validation_data=(X_vali, Y_vali))
