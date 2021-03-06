import tensorflow as tf, numpy as np
from cifarutils import loadCifar

BATCH_SIZE = 256
NUM_EPOCHS = 100

# Fetch dataset
X_train, y_train, X_valid, y_valid, X_test, y_test = loadCifar()
trX, trY, teX, teY = X_train.reshape(len(X_train), -1), y_train, X_test.reshape(len(X_test), -1), y_test

# Create input and output nodes
X = tf.placeholder("float", [None, 3072]) # create symbolic variables
Y = tf.placeholder("float", [None, 10])

w = tf.Variable(tf.random_normal((3072, 10), stddev=0.01))
pred = tf.matmul(X, w)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, Y))
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

predict_op = tf.argmax(pred, 1)
gndtruth_op = tf.argmax(Y, 1)

ispredcorrect = tf.equal(predict_op, gndtruth_op)
accuracy = tf.reduce_mean(tf.cast(ispredcorrect, 'float'))

loss_disp = tf.scalar_summary("Cross entropy", loss)
w_disp = tf.histogram_summary("W", w)
acc_disp = tf.scalar_summary("Accuracy (train)", accuracy)

with tf.name_scope("test") as s:
    accuracy_test = tf.reduce_mean(tf.cast(ispredcorrect, 'float'))
    acc_test_disp = tf.scalar_summary("Accuracy (test)", accuracy_test)

sess = tf.Session()
merged_display = tf.merge_all_summaries()
writer = tf.train.SummaryWriter("/tmp/tflogs_2A", sess.graph_def, flush_secs=10)
init = tf.initialize_all_variables()
sess.run(init)

for i in range(NUM_EPOCHS):
    print(i)
    feed = {X: trX, Y: trY}
    result = sess.run(merged_display, feed_dict=feed)
    writer.add_summary(result, i)
    result = sess.run(acc_test_disp, feed_dict={X: teX, Y: teY})
    writer.add_summary(result, i)
    writer.flush()
    
    #loss.append(sess.run(cost, feed_dict={X: trX, Y: trY}))
    #print(">>>", loss[-1])
    #trainscore.append(np.mean(np.argmax(trY, axis=1) ==
    #                 sess.run(predict_op, feed_dict={X: trX, Y: trY})))
    #print("***", trainscore[-1])
    #testscore.append(np.mean(np.argmax(teY, axis=1) ==
    #                 sess.run(predict_op, feed_dict={X: teX, Y: teY})))
    #print (i, testscore[-1])
    for start, end in zip(range(0, len(trX), BATCH_SIZE),
                            range(BATCH_SIZE, len(trX), BATCH_SIZE)):
        sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})

"""
#w = init_weights([3072, 10]) # like in linear regression, we need a shared variable weight matrix for logistic regression

py_x = model(X, w)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y)) # compute mean cross entropy (softmax is applied internally)
summ1 = tf.scalar_summary("Cross entropy", cost)

train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost) # construct optimizer
predict_op = tf.argmax(py_x, 1) # at predict time, evaluate the argmax of the logistic regression
#summ2 = tf.scalar_summary("Precision", predict_op)


loss, trainscore, testscore = [], [], []
for i in range(NUM_EPOCHS):
    feed = {X: trX, Y: trY}
    result = sess.run([merged], feed_dict=feed)
    summary_str = result[0]
    #acc = result[1]
    writer.add_summary(summary_str, i)
    
    #loss.append(sess.run(cost, feed_dict={X: trX, Y: trY}))
    #print(">>>", loss[-1])
    #trainscore.append(np.mean(np.argmax(trY, axis=1) ==
    #                 sess.run(predict_op, feed_dict={X: trX, Y: trY})))
    #print("***", trainscore[-1])
    #testscore.append(np.mean(np.argmax(teY, axis=1) ==
    #                 sess.run(predict_op, feed_dict={X: teX, Y: teY})))
    #print (i, testscore[-1])
    for start, end in zip(range(0, len(trX), BATCH_SIZE), range(BATCH_SIZE, len(trX), BATCH_SIZE)):
        sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})
"""
