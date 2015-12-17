import numpy as np
import theano
from theano.tensor.nnet import conv
from theano.tensor.shared_randomstreams import RandomStreams
import theano.tensor as T
from theano.tensor.signal import downsample
import pickle

from .visualization import init_learning_curves, update_learning_curves
from .mlp import FullyConnectedLayer, SoftmaxLayer

class ConvLayer(object):
    """Pool Layer of a convolutional network """

    def __init__(self, rng, inputs, filter_shape, image_shape,
                #  stride, pad
                ):
        """
        Allocate a ConvPoolLayer with shared variable internal parameters.

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 4
        :param filter_shape: (number of filters, num input feature maps,
                              filter height, filter width)

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)

        :type poolsize: tuple or list of length 2
        :param poolsize: the downsampling (pooling) factor (#rows, #cols)
        """

        self.input = inputs

        self.W = theano.shared(
            np.random.normal(scale=0.1, size=filter_shape),
            borrow=True
        )

        b_values = np.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        # self.stride = stride
        # self.pad = pad

        conv_out = conv.conv2d(
            input=inputs,
            filters=self.W,
            image_shape=image_shape,
            filter_shape=filter_shape,
        )

        self.output = T.nnet.relu(conv_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        height = image_shape[2] - filter_shape[2] + 1
        width = image_shape[3] - filter_shape[3] + 1
        self.output_shape = (image_shape[0], filter_shape[0], height, width)

        # output_shape_print = theano.printing.Print('conv layer output shape : ')(self.output_shape)

        self.params = [self.W, self.b]

        self.input = inputs


class PoolLayer(object):

    def __init__(self, inputs, input_shape, poolsize=(2,2), stride=(2,2)):
        """
        Allocate a PoolLayer.

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor

        :type poolsize: tuple or list of length 2
        :param poolsize: the downsampling (pooling) factor (#rows, #cols)

        :type stride: tuple or list of length 2
        :param stride: the stride size (#rows, #cols)
        """

        self.input = inputs

        # downsample each feature map individually, using maxpooling
        self.output = T.signal.downsample.max_pool_2d(
            input=inputs,
            ds=poolsize,
            ignore_border=True,
            # st=stride
        )

        if input_shape[2] % 2 == 0:
            height = int(input_shape[2] / 2)
        else:
            height = int((input_shape[2] - 1) / 2)

        if input_shape[3] % 2 == 0:
            width = int(input_shape[3] / 2)
        else:
            width = int((input_shape[3] - 1) / 2)

        self.output_shape = (input_shape[0], input_shape[1], height, width)



class ConvNet(object):

    def __init__(self, train_set_x, train_set_y, valid_set_x, valid_set_y, batch_size, nkerns=[20, 50, 50]):

        nb_channel = train_set_x.shape[1]
        height = train_set_x.shape[2]
        width = train_set_x.shape[3]

        train_set_x = theano.shared(np.asarray(train_set_x, dtype=theano.config.floatX),
                                      borrow=True)
        train_set_y = theano.shared(np.asarray(train_set_y, dtype='int32'),
                                      borrow=True)
        valid_set_x = theano.shared(np.asarray(valid_set_x, dtype=theano.config.floatX),
                                      borrow=True)
        valid_set_y = theano.shared(np.asarray(valid_set_y, dtype='int32'),
                                    borrow=True)

        self.x = T.tensor4('x')
        rng = RandomStreams(seed=465)

        self.layer0 = ConvLayer(
            rng,
            inputs=self.x,
            image_shape=(batch_size, nb_channel, height, width),
            filter_shape=(nkerns[0], nb_channel, 6, 6),
         #    stride=2,
         #    pad=2
        )

        self.layer1 = PoolLayer(
            inputs=self.layer0.output,
            input_shape=self.layer0.output_shape
        )

        self.layer2 = ConvLayer(
            rng,
            inputs=self.layer1.output,
            image_shape=self.layer1.output_shape,
            filter_shape=(nkerns[1], nkerns[0], 6, 6),
         #    stride=2,
         #    pad=2
        )

        self.layer3 = PoolLayer(
            inputs=self.layer2.output,
            input_shape=self.layer2.output_shape
        )

        layer4_input = self.layer3.output.flatten(2)

        n_in = self.layer3.output_shape[1] * self.layer3.output_shape[2] * self.layer3.output_shape[3]
        n_out = int(n_in/2)

        print('aight')
        print(n_in)
        print(n_out)

        self.layer4 = FullyConnectedLayer(layer4_input, n_in, n_out, rng)

        nb_outputs = len(np.unique(train_set_y.get_value()))
        self.layer5 = SoftmaxLayer(inputs=self.layer4.outputs, n_in=n_out, n_out=nb_outputs, rng=rng)

        self.train_set_x = train_set_x
        self.train_set_y = train_set_y
        self.valid_set_x = valid_set_x
        self.valid_set_y = valid_set_y
        self.batch_size = batch_size

    def gradient_descent(self, cost, params, lr, momentum_rate):

        updates = []

        for param in params:

            param_update = theano.shared(param.get_value()*0., broadcastable=param.broadcastable)
            updates.append((param, param - lr*param_update))
            updates.append((param_update, momentum_rate*param_update + (1. - momentum_rate)*T.grad(cost, param)))

        return updates

    def fit(self,
            max_epoch=10,
            learning_rate=0.1, momentum_rate=0,
            weight_decay=0, lambda_1=0,
            curves = False
            ):

        n_train_batch = int(self.train_set_x.get_value(borrow=True).shape[0] / self.batch_size)
        n_valid_batch = int(self.valid_set_x.get_value(borrow=True).shape[0] / self.batch_size)

        print('nb train batches : %d' % n_train_batch)
        print('nb valid batches : %d' % n_valid_batch)

        index = T.lscalar()
        self.y = T.ivector('y')
        lr = T.scalar('lr')

        # create a list of all model parameters to be fit by gradient descent
        params = self.layer5.params + self.layer4.params + self.layer2.params + self.layer0.params

        L2 = (self.layer5.W**2).sum() + (self.layer4.W**2).sum() + (self.layer2.W**2).sum() + \
             (self.layer0.W**2).sum()

        # Cost minimized during training is the NLL of the model
        cost = self.layer5.cost(self.y) + weight_decay * L2

        train_model = theano.function([index, theano.Param(lr, default=learning_rate)],
                                      [cost],
                                      updates = self.gradient_descent(cost, params, lr, momentum_rate),
                                      givens = {
                                              self.x: self.train_set_x[index * self.batch_size:(index + 1) * self.batch_size],
                                              self.y: self.train_set_y[index * self.batch_size: (index + 1) * self.batch_size]
                                              }
                                     )

        train_error = theano.function( [index],
                                       [self.layer5.errors(self.y)],
                                       givens = {
                                            self.x: self.train_set_x[index * self.batch_size:(index + 1) * self.batch_size],
                                            self.y: self.train_set_y[index * self.batch_size: (index + 1) * self.batch_size]
                                       }
                                     )

        valid_error = theano.function( [index],
                                       [self.layer5.errors(self.y)],
                                       givens = {
                                            self.x: self.valid_set_x[index * self.batch_size:(index + 1) * self.batch_size],
                                            self.y: self.valid_set_y[index * self.batch_size: (index + 1) * self.batch_size]
                                       }
                                     )

        print('... training')

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
                                   [self.layer5.y_pred],
                                   givens = {
                                        self.x: test_set_x[index * self.batch_size:(index + 1) * self.batch_size],
                                   }
                                 )

        y_pred = []
        for iter in range(n_test_batch):

            pred = predict(iter)
            y_pred.append(pred)

        return y_pred
