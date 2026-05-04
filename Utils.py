import re
def text_analyze(text):
    if [c for c in text if c.isdigit()]:
        return (False, "Ошибка: Текст содержит цифры.")
    if text == "":
        return (False, "Ошибка: Текст не может быть пустым.")
    pattern = r'[^a-zA-Zа-яА-Я]'
    if re.search(pattern, text):
        return (False, "Ошибка: Текст содержит недопустимые символы.")
    return (True, "Текст корректен.")
def separated(output):
    text = output['text']
    for i in range(len(text)):
        if i % 5 == 0:
            text = text[:i] + " " + text[i:]
    return text