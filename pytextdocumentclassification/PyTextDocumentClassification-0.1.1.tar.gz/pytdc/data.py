import string
import math
import functools
import numpy
import bs4

punctuation_to_strip = string.punctuation.replace("#", "").replace("+", "").replace("-", "")


def normalise_word(word):
    return word.lstrip(punctuation_to_strip).rstrip(punctuation_to_strip).lower()


def word_list_from_document_content(document_content):
    words = [normalise_word(word) for word in document_content.split()]
    return [word for word in words if not word == ""]


def words_from_file(file_object):
    for line in file_object:
        for word in word_list_from_document_content(line):
            yield word


def words_from_email(message):
    def recurse(message_part):
        if message_part.is_multipart():
            parts = [recurse(part) for part in message_part.get_payload()]
            text_plain_parts = [part
                                for part
                                in parts
                                if "text/plain" in part[0].lower()]

            if len(text_plain_parts) > 0:
                return text_plain_parts[0]

            text_html_parts = [part
                                for part
                                in parts
                                if "text/html" in part[0].lower()]

            if len(text_html_parts) > 0:
                return text_html_parts[0]

            return "", []

        else:
            content_type = message_part.get_content_type().lower()
            if "text/plain" in content_type or "text/html" in content_type:
                payload = message_part.get_payload(decode=True)

                html = bs4.BeautifulSoup(payload)
                for style_elem in html.find_all("style"):
                    style_elem.extract()

                lines = [line.strip() for line in html.text.splitlines()]
                line_words_in_lines = [line.split() for line in lines]
                words = [normalise_word(word) for line_words in line_words_in_lines for word in line_words]
                return content_type, [word for word in words if not word == ""]
            else:
                return "", []

    return recurse(message)[1]


def create_classified_data_set(document_vectors, classification_vector):
    return ((document_vector, classification_vector) for document_vector in document_vectors)


def save_classified_data_set(data_set, filename):
    arrays = functools.reduce(lambda acc, data_entry: acc + list(data_entry), data_set, [])
    numpy.savez_compressed(filename, *arrays)


def load_classified_data_set(filename):
    with numpy.load(filename) as data:
        return [(data["arr_%d" % i], data["arr_%d" % (i + 1)]) for i in range(0, len(data.items()), 2)]


def vectorise_words_using_word_vector_model(words, word_vector_model, word_vector_dims):
    def vectorise_word(word):
        return word_vector_model[word] if word in word_vector_model.vocab.keys() else numpy.zeros(word_vector_dims)

    sum_vector = functools.reduce(lambda a, b: a + b, (vectorise_word(word) for word in words), numpy.zeros(word_vector_dims))
    vector_length = sum_vector.dot(sum_vector)
    return sum_vector / math.sqrt(vector_length) if vector_length > 0 else sum_vector
