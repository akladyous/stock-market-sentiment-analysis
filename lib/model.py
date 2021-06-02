from joblib import load
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import tensorflow as tf
from keras.optimizers import Adam
from keras.initializers import zeros
from keras import Sequential, layers
from keras.layers import LSTM, Dense, Embedding, Bidirectional, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class Model(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.model = None
        self.X_test = None
        self.y_test = None
        self.y_encoded = None
        self.y_ohe = None
        self.categories = None
        self.accuracy = None
        self.y_pred = None

    def init(self):
        # l_encoder = LabelEncoder()
        # self.y_encoded = l_encoder.fit_transform(self.y)

        ohe = OneHotEncoder(sparse=False)
        self.y_ohe = ohe.fit_transform(self.y.values.reshape(-1,1))
        self.categories = ohe.categories_[0]

        max_lenght = 100
        tokenizer = Tokenizer(num_words=10_000)
        tokenizer.fit_on_texts(self.X)
        sequences = tokenizer.texts_to_sequences(self.X)
        self.X_test = pad_sequences(sequences, max_lenght)

        embedding_matrix = load('./word2vec/embedding_matrix.pkl')
        BIAS = Model.class_weights_ohe(self.y_ohe)
        METRICS = ['accuracy']
        input_dim = embedding_matrix.shape[0]
        embedding_dim = embedding_matrix.shape[1]
        max_seq_len = self.X_test.shape[1]

        self.model = Model.make_model(metrics=METRICS,
                                    input_dim=input_dim,
                                    embedding_dim=embedding_dim,
                                    weights=embedding_matrix,
                                    input_length=max_seq_len,
                                    output_bias=BIAS
                                    )
        self.model.layers[0].embeddings_initializer = zeros()
        self.model.load_weights('./word2vec/word2vec')
        # return self.model

    def make_prediction(self):
        score = self.model.evaluate(self.X_test, self.y_ohe, batch_size=1, steps=self.X_test.shape[0], verbose=0)
        self.accuracy = score[1]
        self.y_pred = self.model.predict(self.X_test, batch_size=1,verbose=0)
        return self.accuracy, self.y_pred



    @staticmethod
    def make_model(metrics, input_dim, embedding_dim, weights, input_length, output_bias=None):
        if output_bias is not None:
            output_bias = tf.keras.initializers.Constant(output_bias)

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
        model.add(layers.LSTM(16))
        # model.add(GlobalMaxPool1D())
        model.add(Dense(16, activation='relu', name='dense16'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax', bias_initializer=output_bias, name='output4'))

        model.compile(
                    optimizer=Adam(lr=1e-3),
                    loss='CategoricalCrossentropy',
                    metrics=metrics
        )
        return model

    @staticmethod
    def class_weights_ohe(Y_ohe):
        #  n_samples / (n_classes * np.bincount(y))
        # https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html
        bincount = np.array([np.bincount(Y_ohe[:,x].astype(np.int))[1] for x in range(0, Y_ohe.shape[1])])
        weights = np.array(Y_ohe.shape[0] / (Y_ohe.shape[1] * bincount))
        class_weights={k:v for k,v in enumerate(weights)}
        return weights
