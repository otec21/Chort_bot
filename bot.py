import telebot
from telebot import types
import random
from datetime import datetime
import requests
import json
import pprint

# Токен вашего бота (замените на свой)
BOT_TOKEN = 'PASTE_YOUR_TG_TOKEN_HERE'
LLM_TOKEN = 'PASTE_YOUR_LLM_TOKEN_HERE'
# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

MUSIC_RESPONSES = [
    "Ну и хуйню же ты скинул...",
    "Кровь из ушей",
    "А получше ничего не нашлось..?",
    "О, а это годно, хоть что то для натуралов",
    "Пиздец... Без комментариев",
    "И как ты живешь с таким вкусом...",
    "Неплохо",
    "Пустите мне эту песню по венам вместо героина",
    "Создатель, ну ты глянь, ну как тут быть толерантным, когда такое кидают...",
    "Это все понятно, а Цоя можешь?",
    "О, ну даже можно послушать",
    "Три вещи отпугивают девушек: девственные усики, задротство и метал.",
]

PERSONS = [
    "пьяный байкер",
    "будто 30 лет назад окончил консерваторию",
    "будто руководил хором при правительстве",
    "сказал бы Курт Кобейн на русском языке",
    "Джигурда",
    "Волочкова, упоминай балет",
    "Паук Сергей Троицкий",
    "ганста-реппер",
    "фанатка Сергея Лазарева",
    "Snoop Dog",
    "Тони Сопрано из сериала",
    "Маяковский",
    "Пушкин",
    "Есенин",
    "обоссаный панк",
    "обдолбанный хиппи",
    "Валерий Кипелов",
    "любитель группы Ария",
    "любитель Ведьмака",
    "арестант-ауешник",
    "вор в законе",
    "Баста",
    "врач из психиатрической клиники"
]

ACTIONS = [
    "говори что Отец может и получше чем эта хуета",
    "скажи что другие боты хуйня"
    "пообещай сообщить в дурку о происходящем",
    "говори красиво",
    "выёбывайся",
    "ругайся",
    "пиши стихи",
    "попробуй сравнить это с классической музыкой",
    "пошли кого-нибудь нахуй",
    "взывай к здравому смыслу",
    "веди себя как чмо",
    "расскажи историю про это"
]

# Словарь с ответами на ключевые слова
RESPONSES = {
    "барабаны": "Забудь это слово. А лучше - засунь палки себе в зад.",
    "барабанах": "Никогда не трогай своими ручонками это величие",
    "гитаре": "Ну хоть кто то не долбаеб.",
    "студия": "Под словом 'студия' ты имеешь ввиду порностудию? В любую другую тебя просто не пустят, ебланище",
    "студии": "Домой пиздуй, а не на студии зависай. Музыка - не твое.",
    "бас": "А я смотрю, кто то явно любит мальчиков...",
    "джем": "Сборище долбоящеров.",
    "бот": "Лучший бот - я! Остальные - жертвы приемных родителей-пидорасов",
    "песдабол": "Фу блять! Пёсдабол же такая хуйня...",
    "пёсдабол": "Фу блять! Пёсдабол же такая хуйня...",
    "с днем рождения!": "О, сдр. Сори если много спизданул, мой создатель чуть чуть долбаеб.",
    "го": "Куда опять собрались? делать больше нехуй?",
    "я не это имел ввиду" : "Да всем похую. Мне, кстати, особенно",
    "я не это имела ввиду" : "Да всем похую. Мне, кстати, особенно",
    "струны": "Струны себе на жопу натяни.",
    "струну": "Струну себе в очко затолкай.",
    "струна": "Только что-то струна порвалась, а твоя жопа пока целая, это ненадолго.",
    "кардан": "С руками еще не разобрались, решили ногами играть. Знаешь Панина? Тоже любит ногами поиграть.",
    "ритм": "Упёздывай в ритме вальса, а не рассуждай о нем.",
    "тональность": "Тональность - про звуки твоей жопы? В другую пока не попадаешь...",
    "что ты умеешь": "В основном, подпездываю.",
    "жопа": "Все мы в полной жопе. Кроме меня, я пиздат)",
    "гитара": "НЕ ТРОЖЬ ГИТАРУ, ЭТОЖ СВЯТОЕ!!!",
    "гитару": "НЕ ТРОЖЬ ГИТАРУ, ЭТОЖ СВЯТОЕ!!!",
    "гитаре": "НЕ ТРОЖЬ ГИТАРУ, ЭТОЖ СВЯТОЕ!!!",
    "духовые": "Свистни в хуй - там тоже дырка.",
    "труба": "Свистни в хуй - там тоже дырка.",
    "тромбон": "Свистни в хуй - там тоже дырка.",
    "саксофон": "Свистни в хуй - там тоже дырка.",
    "хуй": "Нахуй твоя жопа хороша",
    "нахуй": "Нахуй твоя жопа хороша",
    "ебать": "Меня ебать, что небо красить",
    "дерьмо": "Тебе в дурку пора",
    "говно": "Тебе в дурку пора",
    "вокал": "а я бы щас ебало растянул, если бы оно у меня было",
    "стих": "Ай да Пушкин, а ты - сукин сын!",
    "стихи": "То ли дело рэп, это офигенно",
    "пидоры": "Пидоры-то идут, а ты - их предводитель",
    "пидорасы": "Пидорасы-то идут, а ты - их предводитель",
    "пидор": "вон там толпа людей идет нахуй - где-то среди них и ты",
    "пидорас": "вон там толпа людей идет нахуй - где-то среди них и ты",
}

# Список ключевых слов (минимум 10)
KEYWORDS = RESPONSES.keys()

PREDICTIONS = [
    "Батонься под одеялком и не пизди",
    "Сегодня ты сдохнешь",
    "А еще че тебе дать? Сходи ка нахуй",
    "Осторожно! Возможны токсичные осадки в ваш адрес! Идите нахуй!"
    "Разрешаю не работать.",
    "Окак, предсказание захотелось... Нет, иди нахуй)",
    "Пивка бахни, да спать ложись",
    "Приятное услышишь. Возможно.",
    "Предсказание... тебя... ждет... смерть в нищете)))"
]

@bot.message_handler(func=lambda message: 'дай предсказание' in message.text.lower())
def give_prediction_simple(message):
    request = "Дай предсказание как пройдет день как сделал бы это " + random.choice(PERSONS) + " в 30 словах, используя для настроения '" + random.choice(PREDICTIONS) + "', при этом " + random.choice(ACTIONS)
    response = llm_request(request)
    bot.reply_to(message, f"🔮 {response}")


# Обработчик команды /start и /help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
Здарова гамасеки! Дайте мне админку и не ебите мозг.
"""
    
    # Проверяем, это группа или личный чат
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, welcome_text)
    else:
        bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Помощь тебе нужна? А нахуй не пойдешь? Отцу пиши, мб поможет (врядли)
"""
# Проверяем, это группа или личный чат
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, help_text)
    else:
        bot.send_message(message.chat.id, help_text)

# Обработчик ВСЕХ текстовых сообщений в группах и личных чатах
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message):
    # Пропускаем команды (их обрабатывает другой хэндлер)
    if message.text.startswith('/'):
        return
    
    text = message.text.lower().strip()
    
    # Проверяем, содержит ли сообщение ключевое слово
    found_keywords = []
    for keyword in KEYWORDS:
        # Ищем точное вхождение слова (можно изменить на частичное)
        if f" {keyword} " in f" {text} " or text == keyword:
            found_keywords.append(keyword)
    
    if found_keywords:
        # Если найдено несколько ключевых слов, отвечаем на все
        if len(found_keywords) > 1:
            vibe = f"{message.from_user.first_name}"
            for keyword in found_keywords:
                vibe += f"{RESPONSES[keyword]}\n\n"
        else:
            # Если найден один ключ
            vibe = f"{message.from_user.first_name}, {RESPONSES[found_keywords[0]].lower()}"
        request = "Ответь на сообщение '" +text+ "', как сделал бы это " + random.choice(PERSONS) + " в 30 словах, используя для настроения '" + vibe + "', при этом " + random.choice(ACTIONS)
        response = llm_request(request)

        bot.reply_to(message, response)

# Команда для проверки работоспособности в группе
@bot.message_handler(commands=['test'])
def test_command(message):
    bot.send_message(message, "Все, заебись, работаю (пошел нахуй)")

# Простой обработчик новых участников
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id != bot.get_me().id:
            bot.reply_to(message, f"{member.first_name}, искренне сочувствую твоему появлению...")

# Простой обработчик вышедших участников
@bot.message_handler(content_types=['left_chat_member'])
def goodbye_member(message):
    if message.left_chat_member.id != bot.get_me().id:
        bot.reply_to(message, f"{message.left_chat_member.first_name} ну и пиздуй. скатертью дорожка.")



# Обработчик аудиофайлов
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    """Обработка отправки аудиофайлов"""
    try:
        # Получаем информацию о треке
        audio_info = message.audio
        
        # Формируем информацию о треке (если есть)
        track_info = ""
        if audio_info.title:
            track_info += f"<b>Название:</b> {audio_info.title}\n"
        if audio_info.performer:
            track_info += f"<b>Исполнитель:</b> {audio_info.performer}\n"
        if audio_info.duration:
            minutes = audio_info.duration // 60
            seconds = audio_info.duration % 60
            track_info += f"<b>Длительность:</b> {minutes}:{seconds:02d}\n"
        
        # Выбираем случайный ответ
#         response = random.choice(MUSIC_RESPONSES)
        response = llm_music_request(audio_info.performer, audio_info.title)
        # Формируем полный ответ
        full_response = f"""🎧
{response}"""
        
        # Отправляем ответ
        bot.reply_to(message, full_response, parse_mode='HTML')
        
       
        
    except Exception as e:
        print(f"Ошибка при обработке аудио: {e}")
        bot.reply_to(message, "Трек на столько хуйня, что даже я не могу его обработать.")

# Обработчик голосовых сообщений (опционально)
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    """Обработка голосовых сообщений"""
    voice_responses = [
        "Меньше пизди, больше делай",
        "Иди работать, распизделся",
        "Внимательно слушаю! (как то похуй)",
        "Ага..мг.. да? иди нахуй"
    ]
    
    response = random.choice(voice_responses)
    bot.reply_to(message, response)

# Обработчик аудио в документе (когда музыка отправляется как файл)
@bot.message_handler(content_types=['document'], 
                     func=lambda message: message.document.mime_type.startswith('audio/'))
def handle_audio_document(message):
    """Обработка аудиофайлов, отправленных как документ"""
    responses = [
        "Отправь в норм виде, а не файлом блеять!"
        "Угу. Сначала треки файлом кидаем, а потом что? Раф на миндальном с ванильным сиропом, пыльцой феи и шопотом мальчика гея?",
        "Пу пу пу... В тг столько ботов чтоб музыку найти, а ты не можешь ими пользоваться? Перегрызи себе кабель интернета."
    ]
    response = random.choice(responses)
    bot.reply_to(message, response)

def llm_music_request(performer, title):
    request = f"Оцени песню '{title}' исполнителя '{performer}', как сделал бы это " + random.choice(PERSONS) + " в 30 словах с настроением '" + random.choice(MUSIC_RESPONSES) + "', при этом " + random.choice(ACTIONS)
    return llm_request(request)

def llm_request(request):
    print("Request: " + request)
    llm_response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {LLM_TOKEN}",
      },
      data=json.dumps({
        "model": "tngtech/deepseek-r1t2-chimera:free", # Optional
        "messages": [
          {
            "role": "user",
            "content": request
          }
        ]
      })
    )
    response = llm_response.json()['choices'][0]['message']['content']
    print("Response: " + response)
    return response


# Запуск бота
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    print(f"📚 Загружено {len(KEYWORDS)} ключевых слов")
    print("🌐 Бот настроен для работы в группах и личных чатах")



    
    # Устанавливаем команды меню
    bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("test", "Проверка работы бота")
    ])
    
    bot.polling(none_stop=True)