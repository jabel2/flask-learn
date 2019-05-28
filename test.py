import tensorflow as tf
import keras as k
test = tf.constant("hello")
sess = tf.Session()
print(sess.run(test))
