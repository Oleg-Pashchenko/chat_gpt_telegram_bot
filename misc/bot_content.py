from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

### Messages ###
bot_info = (
    "Добро пожаловать в бота ChatGpt!\nЗдесь ты сможешь получить прогноз на спортивное событие, а также просто"
    " пообщаться с ботом.\nПиши в любое время - мы тебя ждем!"
)
hi_message = "Выбери режим запроса который хочешь совершить:"
predict_message = "Выбран режим прогнозов.\nВведите, что вы хотите узнать:"
normal_mode_message = "Выбран режим обычных запросов.\nВведите, что вы хотите узнать:"
please_wait_message = "Подождите, запрос обрабатывается..."
choose_commands_message = "Введите названия команд (Пример: Реал Мадрид - Ливерпуль):"
choose_date_message = "Введите дату события:"
### Buttons ###
predict_button = InlineKeyboardButton(text="Прогноз", callback_data=f"predict")
normal_mode_button = InlineKeyboardButton(
    text="Обычный режим", callback_data="normal_mode"
)
back_to_menu_button = KeyboardButton(text="Вернуться в меню")
back_to_menu_callback_button = InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu')

### Markups ###
def mode_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(predict_button, normal_mode_button)
    return kb


def back_to_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(back_to_menu_button)
    return kb


### Sports ###
sport_types = {
    "Футбол": "Кто победит? Сколько минимум голов будет забито? Сколько максимум голов будет забито? Обе забьют или нет? Какой будет счёт? Будет ли пенальти? Будет ли гол в первом тайме? Будет ли гол во втором тайме? Обе забьют в первом тайме? Обе забьют во втором тайме? Кто победит в первом тайме? Кто победит во втором тайме?",
    "Баскетбол": "",
    "Теннис": "",
    "Воллейбол": "",
}
sport_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
_sport_row_buttons = []
for i, sport in enumerate(sport_types.keys()):
    _sport_row_buttons.append(InlineKeyboardButton(text=sport, callback_data=sport))
    if len(_sport_row_buttons) == 3:
        sport_keyboard.add(_sport_row_buttons[0], _sport_row_buttons[1], _sport_row_buttons[2])
        _sport_row_buttons = []
if len(_sport_row_buttons) == 1:
    sport_keyboard.add(_sport_row_buttons[0])
if len(_sport_row_buttons) == 2:
    sport_keyboard.add(_sport_row_buttons[0], _sport_row_buttons[1])
sport_keyboard.add(back_to_menu_callback_button)
_sport_row_buttons = []
