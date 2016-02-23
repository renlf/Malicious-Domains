import string
import csv
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import  Convolution1D, MaxPooling1D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
import theano

char_array = [ch for ch in string.ascii_lowercase]
num_array = [str(x) for x in range(0, 10)]
op_array = ['-']
char_array = char_array + num_array + op_array

char_dict = {}
shape_len = 16
train_count = 1400
test_count = 100


def alexa_parser(filename):
    writer = open('top', 'w+')
    csvf = open('top.csv', 'rb')
    reader = csv.reader(csvf)
    for line in reader:
        str = '0.' + line[1]
        writer.write(str + '\n')
    csvf.close()
    writer.close()


def one_hot_encoder():
    array_len = len(char_array)
    for idx, key in enumerate(char_array):
        onehot_array = [0] * array_len
        onehot_array[idx] = 1
        char_dict[key] = onehot_array
    return char_dict


def md_encode(filename, data_count):
    data = np.empty((data_count, shape_len, len(char_array)), dtype="float32")
    label = np.empty((data_count,), dtype="float32")

    reader = open(filename, 'rb')

    for i, line in enumerate(reader):
        domains = line.split('.')
        d_name = domains[1]
        d_labl = domains[0]
        md_data = []

        if len(d_name) > shape_len:
            continue

        for ch in d_name:
            if char_dict.has_key(ch):
                md_data.append(char_dict[ch])
            else:
                md_data.append([0]*len(char_array))

        dim_remain = shape_len - len(d_name)
        while dim_remain > 0:
            md_data.append([0] * len(char_array))
            dim_remain -= 1

        data[i, :, :] = md_data

        if d_labl == '1':
            label[i] = 1
        else:
            label[i] = 0

#        label = np_utils.to_categorical(label, 2)
    return data, label


def md_cnn():
    (X_train, y_train) = md_encode('dn_train', train_count)
    (X_test, y_test) = md_encode('dn_test', test_count)

    model = Sequential()
    model.add(Convolution1D(nb_filter=128, filter_length=2, border_mode='same', activation='tanh', subsample_length=1, input_shape=(shape_len, len(char_array))))#
    model.add(MaxPooling1D(pool_length=2))
    model.add(Convolution1D(nb_filter=128, filter_length=4, border_mode='same', activation='tanh', subsample_length=1))
    model.add(MaxPooling1D(pool_length=2))
#    model.add(Convolution1D(nb_filter=3, filter_length=3, border_mode='same', activation='tanh', subsample_length=1))
#    model.add(MaxPooling1D(pool_length=2))

    model.add(Flatten())

    model.add(Dense(256))
    model.add(Dropout(0.25))
    model.add(Activation('tanh'))

    model.add(Dense(256))
    model.add(Dropout(0.15))
    model.add(Activation('tanh'))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    sgd = SGD(l2=0.0, lr=0.05, decay=1e-6, momentum=0.99, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer=sgd, class_mode='binary')

    get_2nd_layer_output = theano.function([model.layers[0].input], model.layers[2].get_output(train=False))
    layer_output = get_2nd_layer_output(X_train)

    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    hist = model.fit(X_train,y_train, batch_size=128, nb_epoch=256, show_accuracy=True, validation_data=(X_test,y_test))#, callbacks=[early_stopping]) #validation_split=0.2)

 #   print hist.history
 #   print layer_output

#alexa_parser('top.csv')
one_hot_encoder()
#md_encode('dn_train', 500)
md_cnn()
