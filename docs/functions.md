# 6. Функции и рекурсия

<p class="reading-time">Чтение: 5 минут</p>

Функция даёт имя отдельному действию. Это помогает убрать повторения и читать большую программу как последовательность понятных шагов.

## Параметры и `return`

```python
def calculate_total(price, amount):
    return price * amount


total = calculate_total(450, 3)
print(total)
```

`price` и `amount` — параметры. `450` и `3` — аргументы вызова. `return` возвращает значение в программу, а `print()` только показывает его пользователю. Функция без явного `return` возвращает `None`.

## Одна функция — одна задача

Имена вроде `create_field()`, `make_user_move()` и `check_winner()` объясняют сценарий. Полезная функция получает нужные данные параметрами и возвращает результат, а не зависит от случайных глобальных переменных.

```python
def count_ships(field, ship_symbol):
    count = 0
    for row in field:
        for cell in row:
            if cell == ship_symbol:
                count += 1
    return count
```

## Рекурсия

Рекурсивная функция вызывает сама себя. Ей обязательно нужны условие остановки и шаг, приближающий к нему.

```python
def countdown(number):
    if number == 0:
        print("Старт!")
        return
    print(number)
    countdown(number - 1)
```

Для обычного перебора цикл часто проще. Рекурсия полезна, когда задача сама состоит из похожих вложенных подзадач.

## Где это было

- [первые процедуры и функции](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson14_proc_func_1)
- [«Морской бой» после разбиения на функции](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson15_proc_func_2/sea_battle_proc_func.py)
- [примеры рекурсии](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson16_proc_func_3)

## Мини-практика

Разделите игру с полем на функции: создание поля, вывод, безопасный ввод координат, ход и проверка завершения. Главный цикл должен показывать сценарий, а не детали каждой операции.

## Проверьте себя

1. Чем `return` отличается от `print()`?
2. Почему параметры удобнее глобальных переменных?
3. Какие две части обязательны для рекурсии?

[Следующая тема: состояния и файлы →](state-files.md)
