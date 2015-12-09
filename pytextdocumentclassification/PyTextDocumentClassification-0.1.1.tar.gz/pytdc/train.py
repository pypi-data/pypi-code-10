import random


def train_network(network, training_data_set, learning_rate, epoch_length):
    for _ in range(epoch_length):
        training_index = random.randrange(0, len(training_data_set))
        training_input, training_target = training_data_set[training_index]
        weight_and_bias_deltas = network.compute_weight_and_bias_deltas(training_input, training_target, learning_rate)
        network.apply_weight_and_bias_deltas(weight_and_bias_deltas)
