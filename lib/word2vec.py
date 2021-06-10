import numpy as np

def make_model(metrics, input_dim, embedding_dim, weights, input_length): #output_bias=None
    import tensorflow as tf
    from tensorflow.keras.optimizers import Adam
    from keras import Sequential, layers
    from keras.layers import CuDNNLSTM, LSTM, Dense, Embedding, Bidirectional, Dropout
    from keras.losses import categorical_crossentropy
    from keras.layers import GlobalMaxPool1D, LSTM, Dense, Embedding, Bidirectional, Dropout

    # if output_bias is not None:
    #     output_bias = tf.keras.initializers.Constant(output_bias)

    # tf.function(jit_compile=True)
    # tf.compat.v1.enable_eager_execution()
    model = Sequential()
    model.add(
        layers.Embedding(
            input_dim=input_dim, 
            output_dim=embedding_dim,
            weights=[weights],
            input_length=input_length,
            trainable=False,
            mask_zero=True,
            name='embedding'
            )
        )
    model.add(Bidirectional(LSTM(units=embedding_dim, return_sequences=True)))
    # model.add(LSTM(32))
    # model.add(CuDNNLSTM(32))
    # model.add(GlobalMaxPool1D())
    model.add(Dense(16, activation='relu', name='dense16'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax', name='output4'))
    # model.add(Dense(3, activation='softmax', bias_initializer=output_bias, name='output4'))

    model.compile(
                optimizer='adam',
                loss=categorical_crossentropy,
                metrics=metrics
    )
    return model


def class_weights_ohe(Y_ohe):
    #  n_samples / (n_classes * np.bincount(y))
    # https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html
    bincount = np.array([np.bincount(Y_ohe[:,x].astype(np.int))[1] for x in range(0, Y_ohe.shape[1])])
    weights = np.array(Y_ohe.shape[0] / (Y_ohe.shape[1] * bincount))
    class_weights={k:v for k,v in enumerate(weights)}
    return weights

