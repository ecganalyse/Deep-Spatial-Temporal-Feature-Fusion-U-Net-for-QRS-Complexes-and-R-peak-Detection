from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, core, Dropout, concatenate
from tensorflow.keras import layers

def cnnlstm(layer,fitter):

    conv_min = layers.Conv1D(fitter, 3, activation='relu', padding='same', kernel_initializer='he_normal')(layer)
    conv_min = layers.Conv1D(fitter, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv_min)
    conv_min = layers.Conv1D(fitter, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv_min)

    conv_max = layers.Conv1D(fitter, 7, activation='relu', padding='same', kernel_initializer='he_normal')(layer)
    conv_max = layers.Conv1D(fitter, 7, activation='relu', padding='same', kernel_initializer='he_normal')(conv_max)

    lstm1 = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(layer)
    copy = layers.concatenate([conv_min, conv_max, lstm1])

    return copy

def respath(layer,n):
    conv1 = layers.Conv1D(2**(2+n), 3, activation='relu', padding='same', kernel_initializer='he_normal')(layer)
    conv2 = layers.Conv1D(2**(2+n), 1, activation='relu', padding='same', kernel_initializer='he_normal')(layer)
    add = layers.add([conv1, conv2])
    return add

def buildModelSTResUnet(input_length=5000, nChannels=1):
    inputs = Input((input_length,nChannels))
    unet1 = cnnlstm(inputs,8)
    res1 = respath(unet1, 1)
    res1 = respath(res1, 1)
    res1 = respath(res1, 1)
    pool = layers.MaxPool1D(pool_size=2)(unet1)

    unet2 = cnnlstm(pool,16)
    res2 = respath(unet2, 2)
    res2 = respath(res2, 2)
    pool = layers.MaxPool1D(pool_size=2)(unet2)

    unet3 = cnnlstm(pool, 32)
    res3 = respath(unet3,3)
    pool = layers.MaxPool1D(pool_size=2)(unet3)

    unet4 = cnnlstm(pool, 64)
    unet4 = cnnlstm(unet4, 64)

    up3 = layers.UpSampling1D(size=2)(unet4)
    copy3 = layers.concatenate([up3, res3], axis=-1)
    unet3 = cnnlstm(copy3, 32)

    up2 = layers.UpSampling1D(size=2)(unet3)
    copy2 = layers.concatenate([up2, res2], axis=-1)
    unet2 = cnnlstm(copy2, 32)

    up1 = layers.UpSampling1D(size=2)(unet2)
    copy1 = layers.concatenate([up1, res1], axis=-1)
    unet1 = cnnlstm(copy1, 32)

    dense = layers.Dense(1,activation='sigmoid')(unet1)

    model = Model(inputs = inputs,outputs = dense)

    model.summary()

    return model



