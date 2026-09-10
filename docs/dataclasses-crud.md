# 10. `dataclass` и CRUD

<p class="reading-time">Чтение: 5 минут</p>

Когда у сущности много связанных полей, удобнее хранить их в объекте, а не в нескольких списках или словарях.

!!! abstract "Фокус"
    - **Нужно знать:** класс, объект, поле, `@dataclass`, ID и четыре операции CRUD.
    - **Часто в работе:** типы полей, поиск по ID и явный результат операции.
    - **Достаточно узнавать:** `slots=True` и специальные методы класса.

## Модель данных

```python
from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Product:
    name: str
    category: str
    price: int
    rating: float
    amount: int
    release_date: date
    id: int | None = None
```

`@dataclass` создаёт конструктор и понятное строковое представление. `slots=True` не разрешает случайно добавить поле с опечаткой. Аннотация `int | None` означает, что до добавления в каталог ID может отсутствовать.

## Четыре операции CRUD

CRUD — Create, Read, Update, Delete:

```python
def get_product_by_id(products, search_id):
    for product in products:
        if product.id == search_id:
            return product
    return None


def delete_product_by_id(products, search_id):
    product = get_product_by_id(products, search_id)
    if product is None:
        return False
    products.remove(product)
    return True
```

Функция поиска возвращает объект или `None`. Изменение и удаление возвращают `bool`, чтобы UI показал правильное сообщение.

## ID — не индекс

Индекс зависит от позиции в списке и меняется после удаления или сортировки. ID принадлежит объекту и должен оставаться прежним. Новый ID выдаётся отдельным счётчиком.

## Где это было

- [первые модели `Post` и `Product`](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson19_dataclasses_1)
- [каталог автомобилей](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson19_pract)
- [CRUD постов](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson20_dataclasses_2)

## Мини-практика

Создайте `dataclass` `Game` с ID, названием, жанром, ценой и рейтингом. Реализуйте добавление, поиск по ID, изменение цены и удаление.

## Проверьте себя

1. Чем объект удобнее набора несвязанных списков?
2. Почему ID нельзя заменять индексом?
3. Зачем операция удаления возвращает `bool`?

[Следующая тема: архитектура CRUD →](architecture.md)
