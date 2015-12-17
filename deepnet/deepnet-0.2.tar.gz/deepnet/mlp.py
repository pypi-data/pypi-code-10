import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams
import numpy as np
import sys
import pickle
from .visualization import init_learning_curves, update_learning_curves
import os

class FullyConnectedLayer():

    def __init__(self, inputs, n_in, n_out, rng):

        self.inputs = inputs

        self.W = theano.shared(np.random.normal(scale=0.1, size=(n_in, n_out)), borrow=True)
        self.b = theano.shared(np.random.normal(scale=0.1, size=(n_out,)), borrow=True)
        self.params = [self.W, self.b]

        self.outputs = T.nnet.relu(T.dot(self.inputs, self.W) + self.b)

class SoftmaxLayer():

    def __init__(self, inputs, n_in, n_out, rng):

        self.inputs = inputs

        self.W = theano.shared(np.random.normal(scale=0.1, size=(n_in, n_out)), borrow=True)
        self.b = theano.shared(np.random.normal(scale=0.1, size=(n_out,)), borrow=True)
        self.params = [self.W, self.b]

        self.p_y_given_x = T.nnet.softmax(T.dot(self.inputs, self.W)  + self.b)

        self.y_pred = T.argmax(self.p_y_given_x, axis=1)

    def cost(self, y):

        # y_pred_print = theano.printing.Print('y_pred value')(self.outputs)
        # y_print = theano.printing.Print('y_pred value')(y)

        return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])

    def errors(self, y):

        # y_pred_print = theano.printing.Print('y pred value')(self.y_pred)
        # y_print = theano.printing.Print('y target value')(y)

        # return  T.mean(T.neq(y_pred_print, y_print))
        return  T.mean(T.neq(self.y_pred, y))

class MLP():

    def __init__(self, train_set_x, train_set_y, valid_set_x, valid_set_y):

        train_set_x = theano.shared(np.asarray(train_set_x, dtype=theano.config.floatX),
                                      borrow=True)
        train_set_y = theano.shared(np.asarray(train_set_y, dtype='int32'),
                                      borrow=True)
        valid_set_x = theano.shared(np.asarray(valid_set_x, dtype=theano.config.floatX),
                                      borrow=True)
        valid_set_y = theano.shared(np.asarray(valid_set_y, dtype='int32'),
                                    borrow=True)

        self.x = T.dmatrix('x')

        rng = RandomStreams(seed=465)

        nb_features = train_set_x.get_value().shape[1]
        nb_outputs = len(np.unique(train_set_y.get_value()))

        self.fc1 = FullyConnectedLayer(self.x, nb_features, nb_features, rng)
        self.softmax_layer = SoftmaxLayer(self.fc1.outputs, nb_features, nb_outputs, rng)

        self.train_set_x = train_set_x
        self.train_set_y = train_set_y
        self.valid_set_x = valid_set_x
        self.valid_set_y = valid_set_y

    def gradient_descent(self, cost, params, lr, momentum_rate):

        updates = []

        for param in params:

            param_update = theano.shared(param.get_value()*0., broadcastable=param.broadcastable)
            updates.append((param, param - lr*param_update))
            updates.append((param_update, momentum_rate*param_update + (1. - momentum_rate)*T.grad(cost, param)))
            # updates.append((param, param - lr * T.grad(cost, param)))

        return updates

    def fit(self,
              batch_size=200, max_epoch=10,
              learning_rate=0.1, momentum_rate=0,
              weight_decay=0, lambda_1=0,
              curves = False
              ):

        # print('mlp fit')
        self.y = T.ivector('y')
        index = T.lscalar()
        lr = T.scalar('lr')

        self.batch_size = batch_size

        n_train_batch = int(self.train_set_x.get_value(borrow=True).shape[0] / batch_size)
        n_valid_batch = int(self.valid_set_x.get_value(borrow=True).shape[0] / batch_size)

        params = self.fc1.params + self.softmax_layer.params

        L1 = abs(self.fc1.W).sum() + abs(self.softmax_layer.W).sum()
        L2 = (self.fc1.W**2).sum() + (self.softmax_layer.W**2).sum()

        cost = self.softmax_layer.cost(self.y) + weight_decay * L2 + lambda_1 * L1
        # cost = self.softmax_layer.cost(self.y)

        train_model = theano.function([index, theano.Param(lr, default=learning_rate)],
                                      [cost],
                                      updates = self.gradient_descent(cost, params, lr, momentum_rate),
                                      givens = {
                                              self.x: self.train_set_x[index * batch_size:(index + 1) * batch_size],
                                              self.y: self.train_set_y[index * batch_size: (index + 1) * batch_size]
                                              }
                                     )

        train_error = theano.function( [index],
                                       [self.softmax_layer.errors(self.y)],
                                       givens = {
                                            self.x: self.train_set_x[index * batch_size:(index + 1) * batch_size],
                                            self.y: self.train_set_y[index * batch_size: (index + 1) * batch_size]
                                       }
                                     )

        valid_error = theano.function( [index],
                                       [self.softmax_layer.errors(self.y)],
                                       givens = {
                                            self.x: self.valid_set_x[index * batch_size:(index + 1) * batch_size],
                                            self.y: self.valid_set_y[index * batch_size: (index + 1) * batch_size]
                                       }
                                     )
        # print('symbolic function ok')
        train_error_rates = []
        valid_error_rates = []
        nb_epoch = []

        if curves:
            init_learning_curves()

        lr_patience_cpt = 0
        stop_patience_cpt = 0

        lr_patience = 5
        stop_patience = lr_patience*5

        improvement_threshold = 0.995

        best_validation_loss = 100
        best_epoch = 0
        # print('begin real training')
        for epoch in range(max_epoch):

            for iter in range(n_train_batch):

                # print(iter)
                train_model(iter, learning_rate)

            # print(epoch)
            train_losses = [train_error(i) for i
                                 in range(n_train_batch)]
            valid_losses = [valid_error(i) for i
                                 in range(n_valid_batch)]

            train_loss = np.mean(train_losses)
            valid_loss = np.mean(valid_losses)
            train_error_rates.append(train_loss)
            valid_error_rates.append(valid_loss)
            nb_epoch.append(epoch)

            # print('tada')
            if curves:
                update_learning_curves(nb_epoch, train_error_rates, valid_error_rates)
            else:
                # print('check path exist')
                if not os.path.exists('training_outputs'):
                    os.makedirs('training_outputs')
                pickle.dump(nb_epoch, open('training_outputs/nb_epoch.p', 'wb'))
                pickle.dump(train_error_rates, open('training_outputs/train_error_rates.p', 'wb'))
                pickle.dump(valid_error_rates, open('training_outputs/valid_error_rates.p', 'wb'))
                # print('pickle past')

            print('training epoch : %d \n train_loss : %f \n valid_loss : %f' % (epoch, train_loss, valid_loss))

            if valid_loss < best_validation_loss:
                best_validation_loss = valid_loss
                best_epoch = epoch
                pickle.dump(self, open('best_model.p', 'wb'))
                lr_patience_cpt = 0
                stop_patience_cpt = 0
            else:
                lr_patience_cpt += 1
                stop_patience_cpt += 1

            if lr_patience_cpt > lr_patience:

                learning_rate /= 2
                lr_patience_cpt = 0
                print('new learning rate : %f' % learning_rate)
            elif stop_patience_cpt > stop_patience or epoch == max_epoch:
                break

            print(lr_patience_cpt)
            print(stop_patience_cpt)

        return train_error_rates, valid_error_rates


    def predict(self, test_set_x):

        test_set_x = theano.shared(np.asarray(test_set_x, dtype=theano.config.floatX),
                                      borrow=True)

        n_test_batch = int(test_set_x.get_value(borrow=True).shape[0] / self.batch_size)
        index = T.lscalar()

        predict = theano.function( [index],
                                   [self.softmax_layer.y_pred],
                                   givens = {
                                        self.x: test_set_x[index * self.batch_size:(index + 1) * self.batch_size],
                                   }
                                 )

        y_pred = []
        for iter in range(n_test_batch):

            pred = predict(iter)
            y_pred.append(pred)

        return y_pred
