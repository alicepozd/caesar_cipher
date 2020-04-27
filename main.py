from contextlib import suppress
from collections import defaultdict
import string
import argparse
import pickle
import sys


def parse():
    """получение аргументов командной строки"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='mode')

    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'])
    encode_parser.add_argument('--input_file')
    encode_parser.add_argument('--output_file')
    encode_parser.add_argument('--key', default=0)
    encode_parser.set_defaults(func=encode)

    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'])
    decode_parser.add_argument('--input_file')
    decode_parser.add_argument('--output_file')
    decode_parser.add_argument('--key', default=0)
    decode_parser.set_defaults(func=decode)

    hacking_parser = subparsers.add_parser('hacking')
    hacking_parser.add_argument('--cipher', choices=['caesar'])
    hacking_parser.add_argument('--input_file')
    hacking_parser.add_argument('--output_file')
    hacking_parser.add_argument('--frequency_file', default="Alice_frequency.txt")
    hacking_parser.set_defaults(func=hacking)

    count_frequency_parser = subparsers.add_parser('count_frequency')
    count_frequency_parser.add_argument('--input_file')
    count_frequency_parser.add_argument('--output_file')
    count_frequency_parser.set_defaults(func=count_frequency)

    args = parser.parse_args()
    args.func(args)


def count_frequency(args):  # для режима count_frequency (запись в файл)
    d = counting_frequency(args.input_file)
    with open(args.output_file, 'wb') as fout:
            pickle.dump(d, fout)


def counting_frequency(input_file):  # подсчёт частот встречаемости символов
    d = defaultdict(int)
    numb = 0
    fin = sys.stdin
    with suppress(TypeError):
        fin = open(input_file, 'r')
    for line in fin:
        for letter in line:
            if (letter.isalpha()):
                numb += 1
                d[letter.lower()] += 1
    with suppress(TypeError):
        fin.close()
    for elem in d:
        d[elem] /= numb
    return d


def caesar_encode(key, input_file, output_file):  # зашифровка шифр Цезаря
    alfabet_size = 26
    fin = sys.stdin
    fout = sys.stdout
    with suppress(TypeError):
        fin = open(input_file, 'r')
    with suppress(TypeError):
        fout = open(output_file, 'w')
    for line in fin:
        new_line = ""
        for letter in line:
            if (letter.isalpha()):
                letter_numb = string.ascii_lowercase.find(letter.lower())
                new_letter_numb = (letter_numb + key) % alfabet_size
                if (letter.islower()):
                    new_line += string.ascii_lowercase[new_letter_numb]
                else:
                    new_line += string.ascii_uppercase[new_letter_numb]
            else:
                new_line += letter
        fout.write(new_line)
    with suppress(TypeError):
        fin.close()
    with suppress(TypeError):
        fout.close()


def caesar_decode(key, input_file, output_file):  # расшифровка шифр Цезаря
    caesar_encode(-key, input_file, output_file)


def find_distance(d, text_freq, key=0):  # нахождение расстояния между
    alfabet_size = 26                    # двумя частотамм со сдвигом key
    distance = 0
    for i, letter in enumerate(string.ascii_letters):
        text_letter = string.ascii_letters[(i + key) % alfabet_size]
        distance += (d[letter] - text_freq[text_letter])**2
    return distance


def caesar_hacking(args):  # взлом шифр Цезаря
    alfabet_size = 26
    with open(args.frequency_file, 'rb') as fin:
        d = pickle.load(fin)
    text_freq = counting_frequency(args.input_file)
    optimal_distance = find_distance(d, text_freq)
    optimal_key = 0
    for i in range(1, alfabet_size):
        new_distance = find_distance(d, text_freq, i)
        if (new_distance < optimal_distance):
            optimal_distance = new_distance
            optimal_key = i
    caesar_decode(optimal_key, args.input_file, args.output_file)


def vigenere_encode(key, input_file, output_file):  # зашифровка шифр Вижинера
    alfabet_size = 26
    fin = sys.stdin
    fout = sys.stdout
    with suppress(TypeError):
        fin = open(input_file, 'r')
    with suppress(TypeError):
        fout = open(output_file, 'w')
    key_index = 0
    for line in fin:
        new_line = ""
        for letter in line:
            if (letter.isalpha()):
                key_index_numb = string.ascii_uppercase.find(key[key_index])
                letter_numb = string.ascii_lowercase.find(letter.lower())
                new_letter_numb = (letter_numb + key_index_numb) % alfabet_size
                key_index = (key_index + 1) % len(key)
                if (letter.islower()):
                    new_line += string.ascii_lowercase[new_letter_numb]
                else:
                    new_line += string.ascii_uppercase[new_letter_numb]
            else:
                new_line += letter
        fout.write(new_line)
    with suppress(TypeError):
        fin.close()
    with suppress(TypeError):
        fout.close()


def inverse(letter):
    return string.ascii_uppercase[-string.ascii_uppercase.find(letter)]


def vigenere_decode(key, input_file, output_file):  # расшифровка шифр Вижинера
    inverse_key = ''.join(map(inverse, list(key)))
    vigenere_encode(inverse_key, input_file, output_file)


def encode(args):
    if (args.cipher == "caesar"):
        caesar_encode(int(args.key), args.input_file, args.output_file)
    else:
        vigenere_encode(args.key, args.input_file, args.output_file)


def decode(args):
    if (args.cipher == "caesar"):
        caesar_decode(int(args.key), args.input_file, args.output_file)
    else:
        vigenere_decode(args.key, args.input_file, args.output_file)


def hacking(args):
    caesar_hacking(args)


parse()
