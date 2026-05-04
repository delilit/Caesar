import re
def text_analyze(text):
    if [c for c in text if c.isdigit()]:
        return (False, "Ошибка: Текст содержит цифры.")
    if text == "":
        return (False, "Ошибка: Текст не может быть пустым.")
    pattern = r'[^a-zA-Zа-яА-Я\s]'
    if re.search(pattern, text):
        return (False, "Ошибка: Текст содержит недопустимые символы.")
    rus_pattern = r'[а-яА-ЯёЁ]'
    eng_pattern = r'[a-zA-Z]'
    if re.search(rus_pattern, text) and re.search(eng_pattern, text):
        return (False, "Ошибка: Текст содержит смешанные алфавиты.")
    return (True, "Текст корректен.")
def separated(output):
    if type(output) == dict:
        text = output['text']
    else:
        text = output
    
    result = ""
    for i, char in enumerate(text):
        if i > 0 and i % 5 == 0:  # Каждые 5 символов
            result += " "
        result += char
    
    return result