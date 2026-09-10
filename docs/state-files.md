# 9. Конечные автоматы и файлы

<p class="reading-time">Чтение: 5 минут</p>

Состояние отвечает на вопрос: «На каком этапе программа находится сейчас?» Файл позволяет сохранить данные после завершения программы.

!!! abstract "Фокус"
    - **Нужно знать:** состояние, переход, главный цикл, `open`, режимы `r`, `w`, `a` и `with`.
    - **Часто в работе:** отдельные обработчики состояний, формат строки и кодировка UTF-8.
    - **Достаточно узнавать:** диаграммы переходов и сложные форматы файлов.

## Конечный автомат

```python
START = "start"
ROOM = "room"
FINISH = "finish"

state = START

while state != FINISH:
    if state == START:
        print("1. Войти в комнату")
        state = ROOM if input("> ") == "1" else FINISH
    elif state == ROOM:
        print("1. Найти выход")
        state = FINISH if input("> ") == "1" else START
```

У автомата есть конечный набор состояний, события и переходы. Один и тот же ввод может означать разное в разных состояниях. Перед кодом полезно нарисовать переходы стрелками.

## Чтение и запись

```python
with open("scores.txt", "a", encoding="utf-8") as file:
    file.write("Маша;18\n")

with open("scores.txt", "r", encoding="utf-8") as file:
    for line in file:
        name, score = line.strip().split(";")
        print(name, int(score))
```

Режим `r` читает, `w` очищает и записывает заново, `a` добавляет в конец. `with` закрывает файл автоматически. Формат данных нужно договориться заранее: что означает строка и чем разделяются поля.

## Ошибки ввода и файла

```python
try:
    age = int(input("Возраст: "))
except ValueError:
    print("Введите целое число")
```

Ловите конкретную ожидаемую ошибку. Пустой `except:` скрывает и неверный ввод, и ошибку программиста.

## Где это было

- [примеры конечных автоматов](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson16_proc_func_3)
- [текстовый квест](https://github.com/amsmyslov2808/school_11_python_projects/blob/main/lesson16_pract/jailbreak_machine_state.py)
- [работа с текстовыми файлами](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson17_txt_files)

## Мини-практика

Сделайте автомат из трёх экранов: главное меню, просмотр результатов и добавление результата. Список результатов загружайте при старте и сохраняйте после добавления.

## Проверьте себя

1. Что такое состояние и переход?
2. Чем режим `w` опаснее `a`?
3. Почему `except ValueError` лучше пустого `except`?

[Следующая тема: dataclass и CRUD →](dataclasses-crud.md)
