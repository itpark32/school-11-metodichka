# 3. Коллекции и алгоритмы

<p class="reading-time">Чтение: 4 минуты</p>

Список хранит несколько значений в определённом порядке. Индексы начинаются с нуля, поэтому последний допустимый индекс равен `len(items) - 1`.

## Базовые операции

```python
prices = [450, 120, 890]
prices.append(300)
prices[1] = 150

for price in prices:
    print(price)
```

`append()` добавляет в конец, `insert()` — по позиции, `remove()` — по значению, `pop()` — удаляет и возвращает элемент. Перед обращением по индексу проверяйте границы.

## Поиск минимума, максимума и среднего

```python
minimum = prices[0]
maximum = prices[0]
total = 0

for price in prices:
    if price < minimum:
        minimum = price
    if price > maximum:
        maximum = price
    total += price

average = total / len(prices)
```

Алгоритм хранит промежуточное состояние и обновляет его при каждом элементе.

## Пузырьковая сортировка

```python
for end in range(len(prices) - 1, 0, -1):
    for index in range(end):
        if prices[index] > prices[index + 1]:
            prices[index], prices[index + 1] = prices[index + 1], prices[index]
```

Соседние элементы меняются местами. После прохода самое большое значение оказывается справа. Этот учебный алгоритм помогает понять индексы и сравнения; в прикладном коде обычно используют `sorted()` или `.sort()`.

## Где это было

- [операции со списками](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson6_collections)
- [минимум, максимум, среднее и поиск](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson8_collections_algorithms/sample_min_max_avg_search.py)
- [пузырьковая сортировка](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson8_collections_algorithms/sample_bubble_sort.py)

## Мини-практика

Создайте список из десяти случайных оценок от 1 до 5. Найдите минимум, максимум, среднее и количество пятёрок без `min()`, `max()` и `count()`.

## Проверьте себя

1. Почему индекс последнего элемента равен `len(items) - 1`?
2. Чем `remove()` отличается от `pop()`?
3. Почему внутренний цикл сортировки не должен обращаться к несуществующему `index + 1`?

[Следующая тема: двумерные списки и игры →](games.md)
