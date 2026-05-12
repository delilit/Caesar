import re

def text_analyze(text):
    if text == "":
        return (False, "Ошибка: Текст не может быть пустым.")
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