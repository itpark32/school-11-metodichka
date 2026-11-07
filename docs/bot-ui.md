# FSM в Telegram: StateContext, фильтры и многошаговый ввод

<p class="reading-time">Примерное время · Чтение: 6–9 мин · Практика: 60–100 мин</p>

!!! abstract "Фокус"
    - **Нужно знать:** State, StatesGroup, StateMemoryStorage, StateFilter и StateMiddleware.
    - **Нужно уметь:** сохранять данные пользователя между сообщениями и менять шаг после успешной проверки.

## Теория

FSM нужна, когда бот ожидает разные действия на разных этапах. Например: имя клиента → количество → подтверждение. Сообщение 3 может означать количество или пункт меню; текущее состояние задаёт смысл.

### Две разные вещи

Состояние отвечает «что ждём сейчас», данные — «что уже введено». В библиотеке контекст StateContext помогает работать с обоими. У каждого пользователя свой контекст, привязанный к данным события; не заводите единственную переменную state для всех.

### Минимальная настройка библиотеки

```python
import os
import telebot
from telebot import custom_filters
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage

bot = telebot.TeleBot(
    os.environ["TELEGRAM_BOT_TOKEN"],
    state_storage=StateMemoryStorage(),
    use_class_middlewares=True,
    threaded=False,
)
class OrderStates(StatesGroup):
    name = State()
    quantity = State()
    confirmation = State()

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.setup_middleware(StateMiddleware(bot))
```

StateFilter позволяет выбирать handler по state=... . StateMiddleware передаёт в handler аргумент StateContext. Если указать только аннотацию state:StateContext, сам объект из воздуха не появится — нужна настройка middleware.

Threaded=False упрощает последовательное учебное выполнение, но медленный handler задержит всех. StateMemoryStorage хранит данные в памяти; после остановки они исчезают. Это черновик диалога, а не постоянный журнал заказов.

### Операции контекста

| Вызов | Действие |
|---|---|
| state.set(OrderStates.name) | Установить этап |
| state.get() | Прочитать текущий этап |
| state.add_data(name=value) | Добавить временные данные |
| with state.data() as data | Получить накопленные данные |
| state.delete() | Очистить состояние и связанные данные |

Данные сохраняют после валидации. При ошибке отправляют пояснение и return: этап не меняется. На /start можно очистить прежний черновик и начать заново. Отмена тоже должна иметь явный переход.

### Один шаг

Handler получает message и state. Проверяет ввод, добавляет значение, задаёт следующий шаг и отправляет подсказку. Переход к подтверждению не означает автоматическую запись заказа. У подтверждения должен быть отдельный обработчик, вызывающий сервис сохранения.

### Порядок регистрации

Команды /start и /cancel идут перед широкими обработчиками текста. Затем state-фильтры. Сначала объявляются все обработчики, и только в конце запускается bot.infinity_polling(). В упражнениях используйте одного бота и личный чат; темы групп требуют согласования дополнительного контекста.

### Проверка полного пути

Нужны успешный ввод, ошибка на каждом шаге, отмена, повтор /start, два пользователя и повтор нажатия. После state.delete прежняя кнопка не должна сохранять заказ повторно. Долговременную запись подключайте через отдельный сервис.

## Частые ошибки

Не путайте StateFilter и middleware. Не меняйте этап до проверки. Не сохраняйте подтверждённые данные только в памяти FSM. Не запускайте polling до объявления handler.

## Разбор практических задач

Сначала запишите свой план и ожидаемый результат, затем сравните с разбором.

### Задача 1. Начать заново

#### Условие

По /start очистите черновик и запросите имя.

#### Как рассуждать и алгоритм

Фрагмент ставится после настройки bot и до общих handler/polling.

#### Решение

```python
@bot.message_handler(commands=["start"])
def start_order(message, state: StateContext):
    state.delete()
    state.set(OrderStates.name)
    bot.send_message(message.chat.id, "Введите имя клиента")
```

#### Проверка

Повторный /start очищает старые временные данные и возвращает к имени.

### Задача 2. Проверить имя

#### Условие

Принимайте имя 2..30 символов, затем переходите к количеству.

#### Как рассуждать и алгоритм

Неверный ввод оставляет текущее состояние. Сначала сохраните значение, затем смените этап.

#### Решение

```python
@bot.message_handler(state=OrderStates.name, content_types=["text"])
def accept_name(message, state: StateContext):
    name = message.text.strip()
    if not 2 <= len(name) <= 30:
        bot.send_message(message.chat.id, "Нужно имя от 2 до 30 символов")
        return
    state.add_data(name=name)
    state.set(OrderStates.quantity)
    bot.send_message(message.chat.id, "Введите положительное количество")
```

#### Проверка

Пробелы и одна буква отклоняются; Анна сохраняется. Для следующего этапа нужен handler количества.

### Задача 3. Прочитать и отменить

#### Условие

Покажите накопленное имя при /cancel и очистите данные.

#### Как рассуждать и алгоритм

Чтение контекста и удаление выполняются отдельно. Команду зарегистрируйте до обработчиков текста.

#### Решение

```python
@bot.message_handler(commands=["cancel"])
def cancel_order(message, state: StateContext):
    with state.data() as data:
        name = data.get("name", "клиент")
    state.delete()
    bot.send_message(message.chat.id, f"Черновик для {name} отменён")
```

#### Проверка

До ввода имени команда работает с запасным значением. После отмены прежний этап не активен.

## Самостоятельная практика

Добавьте в этот каркас handler количества, вывод черновика и Inline-подтверждение. На подтверждении вызовите переданную функцию сохранения, только после успеха очищайте контекст. Проверьте /cancel, /start и повтор старой кнопки.

## Проверьте себя

1. Что делает middleware?
2. Чем состояние отличается от данных?
3. Что произойдёт после перезапуска?
4. Почему подтверждение требует своего handler?

## Где пригодится и что повторить

PDF №39 и [FSM регистрации](https://github.com/amsmyslov2808/school_11_python_projects/tree/main/lesson34_tg_bot_state_machine). [Синхронный StateContext](https://github.com/eternnoir/pyTelegramBotAPI/blob/master/telebot/states/sync/context.py).

<div class="topic-nav" markdown>

[← Telegram: команды, Reply/Inline-кнопки и обработка действий](bot-events.md)

[ТЗ, макеты и схема переходов Telegram-бота →](bot-design.md)

</div>
