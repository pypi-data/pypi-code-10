import math


def classify_input(network, input_data, positive_classification_predicate):
    input_shape = (network.layers[0].weights.shape[1], 1)
    return positive_classification_predicate(network.compute_outputs(input_data.reshape(input_shape))[-1])


def measure_error(network, test_data_set):
    errors = [network.compute_error(test_input, test_expectation) for test_input, test_expectation in test_data_set]
    return math.fsum(map(lambda x: x ** 2, errors)) / len(errors)


def measure_precision(network, test_data_set, positive_classification_predicate):
    test_outputs = [(network.compute_outputs(test_input)[-1], test_expectation)
                    for test_input, test_expectation
                    in test_data_set]
    results = [positive_classification_predicate(test_expectation)
               for test_output, test_expectation
               in test_outputs
               if positive_classification_predicate(test_output)]
    return len([x for x in results if x])/len(results)


def measure_recall(network, test_data_set, positive_classification_predicate):
    results = [classify_input(network, test_input, positive_classification_predicate)
               for test_input, test_expectation
               in test_data_set
               if positive_classification_predicate(test_expectation)]
    return len([x for x in results if x])/len(results)