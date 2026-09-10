# 6. Строки и срезы

<p class="reading-time">Чтение: 4 минуты</p>

Строка — неизменяемая последовательность символов. Её можно перебирать, искать в ней и брать частями, но нельзя заменить один символ на месте.

!!! abstract "Фокус"
    - **Нужно знать:** индекс, `len`, `in`, `strip`, регистр, `split`, `join` и срез.
    - **Часто в работе:** нормализация текста, поиск части строки и построение новой строки.
    - **Достаточно узнавать:** шифрование текста и расширенные строковые проверки.

## Методы строк

```python
text = "  Python для школьников  "
clean = text.strip().lower()

print(len(clean))
print("python" in clean)
print(clean.replace("python", "питон"))
print(clean.split())
```

Часто нужны `strip()`, `lower()`, `upper()`, `find()`, `replace()`, `split()` и `join()`.

## Срез

Запись `value[start:stop:step]` берёт часть строки или списка. Правая граница не включается.

```python
word = "программирование"

print(word[:6])
print(word[6:])
print(word[::2])
print(word[::-1])
```

## Шифр Цезаря

Вместо длинной цепочки условий можно найти индекс буквы в алфавите, прибавить ключ и взять остаток от длины алфавита:

```python
new_index = (old_index + key) % len(ALPHABET)
encrypted += ALPHABET[new_index]
```

Остаток `%` возвращает индекс в начало алфавита после его конца. Незнакомые символы можно оставить без изменения.

## Где это было

- [первые операции со строками](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson12_strings)
- [шифр Цезаря](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson13_srings_cezar_pole_chudes/cezar.py)
- [цензор текста](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson13_srings_cezar_pole_chudes/censor.py)
- [игра «Поле чудес»](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson13_dops/pole_chudes.py)

## Мини-практика

Нормализуйте фразу: уберите пробелы по краям, переведите в нижний регистр и удалите пробелы внутри. Проверьте срезом, является ли результат палиндромом.

## Проверьте себя

1. Почему нельзя написать `word[0] = "П"`?
2. Что означает пустая часть в `word[:5]`?
3. Зачем в шифре Цезаря оператор `%`?

[Следующая тема: функции →](functions.md)
