# 15. Lambda-функции и генераторы коллекций

<p class="reading-time">Чтение: 8 минут</p>

Lambda и генераторы коллекций делают короткие преобразования, поиск и сортировку компактнее. Сначала нужно уметь написать обычный цикл — тогда сокращенная запись остается понятной.

!!! abstract "Фокус"
    - **Нужно знать:** функция как значение, `lambda`, list comprehension, условие внутри генератора.
    - **Часто в работе:** `key` для сортировки, фильтрация и преобразование списка.
    - **Достаточно узнавать:** вложенные генераторы и длинные lambda-выражения.

## Функция как аргумент

```python
def calculate(a, b, action):
    return action(a, b)


result = calculate(8, 3, lambda x, y: x - y)
print(result)  # 5
```

Параметр `action` хранит функцию. `lambda x, y: x - y` принимает два аргумента и возвращает результат выражения.

Lambda подходит для одного короткого действия. Если нужна проверка, цикл или несколько шагов, обычная функция с понятным именем читается лучше.

## Сортировка по ключу

```python
products.sort(key=lambda product: product.price)
products.sort(key=lambda product: product.rating, reverse=True)
```

`key` не сравнивает объекты сам. Для каждого объекта он вычисляет значение, по которому Python построит порядок.

## Генератор списка

```python
numbers = [2, 3, 5, 6, 8]
squares_of_even = [number ** 2 for number in numbers if number % 2 == 0]

print(squares_of_even)  # [4, 36, 64]
```

Читайте выражение по частям:

1. `for number in numbers` — перебираем числа;
2. `if number % 2 == 0` — оставляем четные;
3. `number ** 2` — добавляем квадрат в новый список.

Тот же принцип используется для поиска объектов:

```python
found = [
    product
    for product in products
    if query.lower() in product.name.lower()
]
```

!!! warning "Ловушка: слишком много логики в одной строке"
    Если выражение приходится долго расшифровывать, вернитесь к обычному циклу или вынесите условие в именованную функцию.

## Где это было

- [первые lambda-функции](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson27_lambda_generators/sample1.py)
- [генератор списка](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson27_lambda_generators/sample2.py)
- [сортировка и фильтрация большого каталога](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson27_big_project_7/buyer_menu.py)

## Мини-практика

Из списка игр получите только игры с рейтингом не ниже 4, затем отсортируйте их по цене. Сначала решите задачу обычным циклом, потом генератором списка и `sort(key=...)`.

## Проверьте себя

1. Что принимает и что возвращает lambda-функция?
2. Для чего сортировке параметр `key`?
3. В каком порядке удобно читать генератор списка?
4. Когда обычная функция понятнее lambda?

[Следующая тема: Git и история проекта](git.md)
