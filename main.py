from contextlib import contextmanager
from collections import defaultdict
import string
import argparse
import pickle
import math
import sys


@contextmanager
def file_open(name, mode):
    try:
        if name is None:
            if mode == 'r':
                yield sys.stdin
            yield sys.stdout
        open_file = open(name, mode)
        yield open_file
    finally:
        if name:
            open_file.close()


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='mode')

    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], required=True,
                               help='cipher: выбор из caesar или vigenere')
    encode_parser.add_argument('--input_file',
                               help='input_file: если не указан, ввод через sys.stdin')
    encode_parser.add_argument('--output_file',
                               help='output_file если не указан, вывод через sys.stdout')
    encode_parser.add_argument('--key', required=True,
                               help='key, обязательный аргумент: число для caesar, строка для vigenere')
    encode_parser.set_defaults(func=encode)

    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], required=True,
                               help='cipher: выбор из caesar или vigenere')
    decode_parser.add_argument('--input_file',
                               help='input_file: если не указан, ввод через sys.stdin')
    decode_parser.add_argument('--output_file',
                               help='output_file: если не указан, вывод через sys.stdout')
    decode_parser.add_argument('--key', required=True,
                               help='key, обязательный аргумент: число для caesar, строка для vigenere')
    decode_parser.set_defaults(func=decode)

    hacking_parser = subparsers.add_parser('hacking')
    hacking_parser.add_argument('--cipher', choices=['caesar'], required=True,
                                help='cipher: выбор из caesar или vigenere')
    hacking_parser.add_argument('--input_file',
                                help='input_file: если не указан, ввод через sys.stdi')
    hacking_parser.add_argument('--output_file',
                                help='output_file: если не указан, вывод через sys.stdout')
    hacking_parser.add_argument('--frequency_file', default="Alice_frequency.txt",
                                help='frequency_file если не указан, используется Alice_frequency.txt')
    hacking_parser.set_defaults(func=caesar_hacking)

    count_frequency_parser = subparsers.add_parser('count_frequency')
    count_frequency_parser.add_argument('--input_file',
                                        help='input_file: если не указан, ввод через sys.stdin')
    count_frequency_parser.add_argument('--output_file', required=True,
                                        help='output_file: обязательный аргумент')
    count_frequency_parser.set_defaults(func=count_frequency)

    args = parser.parse_args()
    return args


def make_alphabet_dict():
    return {letter: ind for ind, letter in enumerate(string.ascii_letters)}


def count_frequency(args):
    '''для режима count_frequency (запись в файл)'''
    dictionary = counting_frequency(args.input_file)
    with open(args.output_file, 'wb') as output_file:
        pickle.dump(dictionary, output_file)


def counting_frequency(input_file):
    '''подсчёт частот встречаемости символов'''
    alphabet_dict = make_alphabet_dict()
    dictionary = defaultdict(int)
    with file_open(input_file, 'r') as input_file:
        for line in input_file:
            for letter in line:
                if letter in alphabet_dict:
                    dictionary[letter.lower()] += 1
    number_of_letters = sum(dictionary.values())
    for elem in dictionary:
        dictionary[elem] /= number_of_letters
    return dictionary


def caesar_encode_function(letter, key, numb_of_letter, alphabet_dict):
    letter_numb = alphabet_dict[letter.lower()]
    new_letter_numb = (letter_numb + key) % len(string.ascii_lowercase)
    return new_letter_numb


def vigenere_encode_function(letter, key, numb_of_letter, alphabet_dict):
    key_index_numb = alphabet_dict[key[numb_of_letter % len(key)].lower()]
    letter_numb = alphabet_dict[letter.lower()]
    new_letter_numb = (letter_numb + key_index_numb) % len(string.ascii_lowercase)
    return new_letter_numb


def encode_text(key, encode_function, input_file, output_file):
    alphabet_dict = make_alphabet_dict()
    with file_open(input_file, 'r') as input_file:
        with file_open(output_file, 'w') as output_file:
            number_of_letters = 0
            for line in input_file:
                new_line = []
                for letter in line:
                    if letter in alphabet_dict:
                        new_letter_numb = encode_function(letter, key, number_of_letters, alphabet_dict)
                        number_of_letters += 1
                        if letter.islower():
                            new_line.append(string.ascii_lowercase[new_letter_numb])
                        else:
                            new_line.append(string.ascii_uppercase[new_letter_numb])
                    else:
                        new_line.append(letter)
                output_file.write(''.join(new_line))


def caesar_decode(key, input_file, output_file):
    encode_text(-key, caesar_encode_function, input_file, output_file)


def find_distance(dictionary, text_freq, key=0):
    '''нахождение расстояния между двумя частотами со сдвигом key'''
    distance = 0
    for shift, letter in enumerate(string.ascii_letters):
        text_letter = string.ascii_letters[(shift + key) % len(string.ascii_lowercase)]
        distance += (dictionary[letter] - text_freq[text_letter])**2
    return distance


def caesar_hacking(args):
    with open(args.frequency_file, 'rb') as input_file:
        dictionary = pickle.load(input_file)
    text_freq = counting_frequency(args.input_file)
    optimal_distance = math.inf
    for shift in range(0, len(string.ascii_lowercase)):
        new_distance = find_distance(dictionary, text_freq, shift)
        if new_distance < optimal_distance:
            optimal_distance = new_distance
            optimal_key = shift
    caesar_decode(optimal_key, args.input_file, args.output_file)


def inverse(letter):
    alphabet_dict = make_alphabet_dict()
    if letter.lower() == 'a':
        return letter
    letter_numb = len(string.ascii_lowercase) - alphabet_dict[letter]
    return string.ascii_lowercase[letter_numb]


def vigenere_decode(key, input_file, output_file):
    inverse_key = ''.join(map(inverse, key))
    encode_text(inverse_key, vigenere_encode_function, input_file, output_file)


def encode(args):
    if args.cipher == "caesar":
        encode_text(int(args.key), caesar_encode_function, args.input_file, args.output_file)
    else:
        encode_text(args.key, vigenere_encode_function, args.input_file, args.output_file)


def decode(args):
    if args.cipher == "caesar":
        caesar_decode(int(args.key), args.input_file, args.output_file)
    else:
        vigenere_decode(args.key, args.input_file, args.output_file)


if __name__ == '__main__':
    args = parse_command_line_args()
    args.func(args)
