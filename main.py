from pprint import pprint
import re

from PyPDF2 import PdfReader


def readaerFile():
    '''
    Считываем локальный пдф - файл
    :return:
    '''
    reader = PdfReader('file/test_task.pdf')
    page = reader.pages[0]
    return page.extract_text().splitlines()

def search_digit(l: list):
    '''
    Проверяем что value от друого key не сцепились к друг другу
    :param l: Принимаем строку из пдф файла в формате List
    :return: Возвращаем число если такое было найдено
    '''
    for i in l:
        if ':' in i:
            for j in i:
                if j.isdigit():
                    return j
                else:
                    continue

def separate_number_string(l: list):
    '''
    Если функция search_digit in not None тогда эта функция расцепляет число и строку на две строки
    :param l: Принимаем строку из пдф файла в формате List
    :return: Возвращаем отформатированную строку
    '''
    separated_strings = []
    for string in l:
        separated_string = re.findall(r'(\d+|\D+)', string)
        separated_strings.extend(separated_string)
    return separated_strings

def createDictv2():
    '''
    Функция создает словарь из значений которые были в пдф
    :return: Возвращает словарь
    '''
    dict_info = dict(COMPANY=readaerFile()[0])
    for i in readaerFile()[1:-1]:
        i = i.replace('# :', '#:') # для определения key нам требуется убрать пробел между символами
        if ' ' in i[:i.find(':')]: # убираем пробелы в key
            i = i[:i.find(':')].replace(' ', '_') + i[i.find(':'):]
        split_i = i.split()
        if search_digit(split_i) is not None: # проверка на цифры в массиве ( см доку фукнции )
            split_i = separate_number_string(split_i)
        for j in split_i:
            if ':' in j:
                dict_info[j[:-1]] = None # добавляем key без ':' с значением None на тот случай если value не проставлено
                last_j = j # сохраняем переменную чтобы переопределить key если value проставлено
            else:
                if ':' in last_j:
                    dict_info[last_j[:-1]] = j # проверяем если last_j было ключем ( есть внутри символ ':' ), то j это вэлью
    dict_info['NOTES'] = readaerFile()[-1] # добавляем текст в нотес

    return dict_info


pprint(createDictv2())





