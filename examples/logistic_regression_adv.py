from minpy import core
import minpy.numpy as np
import mxnet as mx

def sigmoid(x):
    return np.multiply(0.5, np.add(np.tanh(x), 1))

x = mx.sym.Variable(name='x')
fc = mx.sym.FullyConnected(name='fc', data=x)
#fc = mx.sym.FullyConnected(name='fc', data=x, num_hidden=inputs.shape[1])
act = mx.sym.Activation(data=fc, act_type='sigmoid'）
f = core.function(act)

def predict(weights, inputs):
    return f(x=inputs, fc_weight=weights, ctx=mx.cpu())

def training_loss(weights, inputs):
    preds = predict(weights, inputs)
    label_probabilities = preds * targets + (1 - preds) * (1 - targets)
    return -np.sum(np.log(label_probabilities))

xshape = (256, 500)
wshape = (500, 250)
tshape = (256, 250)
inputs = np.random.rand(*xshape) - 0.5
targets = np.random.randint(0, 2, size=tshape)
weights = np.random.rand(*wshape) - 0.5

training_gradient_fun = core.grad(training_loss)

print('Initial loss: {}'.format(training_loss(weights, inputs)))
for i in range(100):
    gr = training_gradient_fun(weights, inputs)
    #print('Training gradient: {}'.format(gr))
    weights -= gr * 0.1
    if i % 10 == 0:
        print('Trained loss: {}'.format(training_loss(weights, inputs)))