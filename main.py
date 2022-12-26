from PIL import Image, ImageDraw
from random import randint
from PIL import Image
from re import findall


def stega_encrypt(old_file: str, new_file: str, key_file: str = 'keys.txt') -> None:
    img = Image.open(old_file)
    draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pix = img.load()
    #  Самая главная задача — придумать способ, по средством которого станет возможным шифровать сообщения.
    #  Мною был предложен такой способ:
    #
    # Берем символ, переводим его в число ASCII.
    # Создаём кортеж со случайными значениями координат.
    # Собираем зелёный и синий оттенки из пикселя по координатам.
    # Заменяем красный оттенок на номер символа по ASCII.
    with open(key_file, encoding='utf-8', mode='w') as file:
        for elem in ([ord(elem) for elem in input('Введите текст: ')]):
            key = (randint(1, width - 10), randint(1, height - 10))
            g, b = pix[key][1:3]
            draw.point(key, (elem, g, b))
            file.write(str(key) + '\n')
        # Сохраняем ключи и изображение.
        print('Ключи были записаны в keys.txt')
        img.save(new_file, 'PNG')


def stega_decrypt(new_file: str, key_file: str) -> str:
    a: list = []
    keys: list = []
    img = Image.open(new_file)
    pix = img.load()
    with open(key_file, encoding='utf-8', mode='r') as file:
        y: str = str([line.strip() for line in file])
        # Основной алгоритм расшифровки:
        for i in range(len(findall(r'\((\d+),', y))):
            # Указанные регулярные выражения нужны для считывания кортежей из текстового файла.
            keys.append((int(findall(r'\((\d+),', y)[i]), int(findall(r',\s(\d+)\)', y)[i])))
        for key in keys:
            a.append(pix[tuple(key)][0])
        return ''.join([chr(elem) for elem in a])


def main():
    old_path: str = 'Image.png'
    new_path: str = 'NewImage.png'
    key_file: str = 'keys.txt'
    stega_encrypt(old_path, new_path, key_file)
    print(f'Ваше сообщение: {stega_decrypt(new_path, key_file)}')
    # Что и требовалось доказать, всё работает!
    #
    # Главный недостаток: видимость битых пикселей изображения в случае шифрования большого количества символов.
    # Однако, этот недостаток отлично исправляется высоким разрешением.


if __name__ == '__main__':
    main()
