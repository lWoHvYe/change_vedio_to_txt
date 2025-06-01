import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import BinaryCrossentropy

if __name__ == '__main__':
    x = np.array([[200.0, 1.77], [180, 2.3], [260, 2.5]])
    layer_1 = Dense(units=3, activation='sigmoid')
    layer_2 = Dense(units=5, activation='sigmoid')
    layer_3 = Dense(units=3, activation='sigmoid')
    layer_4 = Dense(units=1, activation='sigmoid')
    layer_5 = Dense(units=1, activation='sigmoid')
    a1 = layer_1(x)
    a2 = layer_2(a1)
    a3 = layer_3(a2)
    a4 = layer_4(a3)
    a5 = layer_5(a4)

    print(a4)
    print(a5)

    X = np.array([
        [0.1, 0.5],
        [0.3, 0.7],
        [0.6, 0.9],
        [0.4, 0.2],
        [0.8, 0.1],
        [0.05, 0.4],
        [0.9, 0.8],
        [0.2, 0.3],
        [0.7, 0.6],
        [0.3, 0.2]
    ], dtype=np.float32)
    Y = np.array([0, 0, 1, 0, 1, 0, 1, 0, 1, 0], dtype=np.float32)
    model = Sequential([
        Dense(units=3, activation='sigmoid'),
        Dense(units=5, activation='sigmoid'),
        Dense(units=1, activation='sigmoid')
    ])
    model.compile(loss=BinaryCrossentropy())
    model.fit(X, Y, epochs=100)

    model = Sequential([
        Dense(units=3, activation='sigmoid'),
        Dense(units=5, activation='sigmoid'),
        Dense(units=1, activation='linear')
    ])
    model.compile(optimizer='adam', loss=BinaryCrossentropy(from_logits=True))
    model.fit(X, Y, epochs=100)
    logit = model(X)
    f_x = tf.nn.sigmoid(logit)
    print(f_x)

#   W是一个矩阵
#   W[:, j] 表示第j列的所有行
#   W[i, :] 表示第i行的所有列

X = np.array([[200, 17]])  # 1 * 2
W = np.array([[1, -3, 5], [-2, 4, -6]])  # 2 * 3
B = np.array([[-1, 1, 2]])


def dense(A_in, W, B):
    Z = np.matmul(A_in, W) + B
    # Z = A_in @ W
    # g is sigmoid function
    A_out = g(Z)
    return A_out


def g(Z):
    return 1 / (1 + np.exp(-Z))


print(dense(X, W, B))


w = tf.Variable(0, dtype=tf.float32)
optimizer = tf.keras.optimizers.Adam(0.1)

def train_step():
    with tf.GradientTape() as tape:
        cost = w ** 2  - 10 * w + 25
    trainable_variables = [w]
    gradients = tape.gradient(cost, trainable_variables)
    optimizer.apply_gradients(zip(gradients, trainable_variables))
print(w)
for i in range(100):
    train_step()
print(w)
