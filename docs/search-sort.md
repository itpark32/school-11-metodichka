# 11. Сортировка и поиск

<p class="reading-time">Чтение: 5 минут</p>

Поиск создаёт выборку подходящих объектов. Сортировка меняет их порядок. У пользователя должен быть явный критерий для каждой операции.

## Поиск по части текста

```python
def find_by_name(products, query):
    result = []
    query = query.strip().lower()

    for product in products:
        if query in product.name.lower():
            result.append(product)

    return result
```

`strip()` убирает пробелы по краям, а `lower()` делает поиск независимым от регистра. Функция возвращает пустой список, если совпадений нет: это нормальный результат, а не авария.

## Поиск по диапазону

```python
def find_by_price(products, min_price, max_price):
    found = []
    for product in products:
        if min_price <= product.price <= max_price:
            found.append(product)
    return found
```

До поиска проверьте, что нижняя граница не больше верхней.

## Сортировка объектов

Учебный проект вручную сравнивает соседние объекты по `price`, `rating`, `release_date` или `id`. В обычном прикладном коде ту же задачу короче выражает ключ:

```python
products.sort(key=lambda product: product.price)
products.sort(key=lambda product: product.rating, reverse=True)
```

`key` отвечает «какое значение сравнивать», `reverse=True` — «идти по убыванию».

## Где это было

- [учебная пузырьковая сортировка чисел](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson8_collections_algorithms/sample_bubble_sort.py)
- [поиск и восемь сортировок объектов](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson26_big_project_6/products_functions.py)

## Мини-практика

Для каталога игр реализуйте поиск по части названия, точному жанру и диапазону рейтинга. Добавьте сортировку по цене в обоих направлениях.

## Проверьте себя

1. Почему поиск возвращает список, а поиск по ID — один объект или `None`?
2. Для чего одинаково нормализовать запрос и значение?
3. Что задают `key` и `reverse`?

[Следующая тема: консольный UI →](ui.md)
