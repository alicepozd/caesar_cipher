import argparse
import pickle
import sys


def Parse():  # получение аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('type', nargs=1)
    parser.add_argument('--input_file', default="sys.stdin")
    parser.add_argument('--output_file', default="sys.stdout")
    parser.add_argument('--frequency_file', default="Alice_frequency")
    parser.add_argument('--cipher')
    parser.add_argument('--key')
    args = parser.parse_args()
    return args


def Is_small_lat(letter):
    return (letter >= "a") and (letter <= "z")


def Is_big_lat(letter):
    return (letter >= "A") and (letter <= "Z")


def s_lat_n(letter):
    return ord(letter) - ord("a")


def b_lat_n(letter):
    return ord(letter) - ord("A")


def make_s_lat(numb):
    return chr(ord("a") + numb)


def make_b_lat(numb):
    return chr(ord("A") + numb)


def count_frequency():  # для режима count_frequency (запись в файл)
    d = counting_frequency()
    with open(args.output_file, 'wb') as fout:
            pickle.dump(d, fout)


def counting_frequency():  # подсчёт частот встречаемости символов
    d = dict()
    Numb = 0
    if (args.input_file != "sys.stdin"):
        fin = open(args.input_file, 'r')
    else:
        fin = sys.stdin
    for line in fin:
        for i in range(len(line)):
            if (Is_big_lat(line[i]) or Is_small_lat(line[i])):
                Numb += 1
                if line[i] in d:
                    d[line[i]] += 1
                else:
                    d[line[i]] = 1
    if (args.input_file != "sys.stdin"):
        fin.close()
    return [d, Numb]


def caesar_encode(key):  # зашифровка шифр Цезаря
    if (args.input_file != "sys.stdin"):
        fin = open(args.input_file, 'r')
    else:
        fin = sys.stdin
    if (args.output_file != "sys.stdout"):
        fout = open(args.output_file, 'w')
    else:
        fout = sys.stdout
    for line in fin:
        for i in range(len(line)):
            if (Is_big_lat(line[i])):
                letter_numb = (b_lat_n(line[i]) + int(key)) % 26
                fout.write(make_b_lat(letter_numb))
            elif (Is_small_lat(line[i])):
                letter_numb = (s_lat_n(line[i]) + int(key)) % 26
                fout.write(make_s_lat(letter_numb))
            else:
                fout.write(line[i])
    if (args.input_file != "sys.stdin"):
        fin.close()
    if (args.output_file != "sys.stdout"):
        fout.close()


def caesar_decode(key):  # расшифровка шифр Цезаря
    caesar_encode(str(int(key)*(-1)))


def find_distance(d, text_freq, key=0):  # нахождение расстояния между
    distance = 0                         # двумя частотамм со сдвигом key
    for i in range(26):
        d_freq = 0
        t_freq = 0
        letter = (i + key) % 26
        if make_s_lat(i) in d[0]:
            d_freq += d[0][make_s_lat(i)]
        if make_b_lat(i) in d[0]:
            d_freq += d[0][make_b_lat(i)]
        if make_s_lat(letter) in text_freq[0]:
            t_freq += text_freq[0][make_s_lat(letter)]
        if make_b_lat(letter) in text_freq[0]:
            t_freq += text_freq[0][make_b_lat(letter)]
        distance += (d_freq * text_freq[1] - t_freq * d[1])**2
    return distance


def caesar_hacking():  # взлом шифр Цезаря
    with open(args.frequency_file, 'rb') as fin:
        d = pickle.load(fin)
    text_freq = counting_frequency()
    opt_distance = find_distance(d, text_freq)
    opt_key = 0
    for i in range(1, 26):
        new_distance = find_distance(d, text_freq, i)
        if (new_distance < opt_distance):
            opt_distance = new_distance
            opt_key = i
    caesar_decode(opt_key)


def vigenere_encode(key):  # зашифровка шифр Вижинера
    if (args.input_file != "sys.stdin"):
        fin = open(args.input_file, 'r')
    else:
        fin = sys.stdin
    if (args.output_file != "sys.stdout"):
        fout = open(args.output_file, 'w')
    else:
        fout = sys.stdout
    key_index = 0
    for line in fin:
        for i in range(len(line)):
            if (Is_big_lat(line[i])):
                key_index_numb = b_lat_n(key[key_index])
                letter_numb = (b_lat_n(line[i]) + key_index_numb) % 26
                fout.write(make_b_lat(letter_numb))
                key_index = (key_index + 1) % len(key)
            elif (Is_small_lat(line[i])):
                key_index_numb = b_lat_n(key[key_index])
                letter_numb = (s_lat_n(line[i]) + key_index_numb) % 26
                fout.write(make_s_lat(letter_numb))
                key_index = (key_index + 1) % len(key)
            else:
                fout.write(line[i])
    if (args.input_file != "sys.stdin"):
        fin.close()
    if (args.output_file != "sys.stdout"):
        fout.close()


def vigenere_decode(key):  # расшифровка шифр Вижинера
    new_key = ''
    for i in range(len(key)):
        new_key += chr(26 - ord(key[i]) + 2 * ord("A"))
    vigenere_encode(new_key)


args = Parse()
if (args.type[0] == "encode"):
    if (args.cipher == "caesar"):
        caesar_encode(args.key)
    else:
        vigenere_encode(args.key)
elif (args.type[0] == "decode"):
    if (args.cipher == "caesar"):
        caesar_decode(args.key)
    else:
        vigenere_decode(args.key)
elif (args.type[0] == "hacking"):
    if (args.cipher == "caesar"):
        caesar_hacking()
elif (args.type[0] == "count_frequency"):
    count_frequency()
