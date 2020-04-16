Выбранный вариант проекта - шифрование.
Проект лежит в ветке dev.

Режимы и их запуск:
1) Шифрование:
python3 main.py encode --input_file <path_1> --output_file <path_2> --cipher <caesar или vigenere> --key <ключ шифра: число в случае Цезаря, слово в случае Виженера>
Ключа и шифра по умолчанию нет. Если не указан input_file/output_file, то ввод/вывод будет производиться через консоль.
2) Дешифрование:
python3 main.py decode --input_file <path_1> --output_file <path_2> --cipher <caesar или vigenere> --key <ключ шифра: число в случае Цезаря, слово в случае Виженера>
Ключа и шифра по умолчанию нет. Если не указан input_file/output_file, то ввод/вывод будет производиться через консоль.
3) Подсчёт частот символов:
python3 main.py count_frequency --input_file <path_1> --output_file <path_2>
output_file по умолчанию нет. Если не указан input_file, то ввод будет производиться через консоль.
4) Взлом шифра Цезаря:
python3 main.py hacking --input_file <path_1> --output_file <path_2> --frequency_file <path_3> --cipher <caesar>
Если не указан input_file/output_file, то ввод/вывод будет производиться через консоль. Если не указан frequency_file будет использоваться Alice_frequency.txt
