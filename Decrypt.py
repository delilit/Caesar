import re
from collections import Counter

RUS_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
RUS_FREQ = {
    'а': 0.062,'б': 0.014,'в': 0.038,'г': 0.013,'д': 0.025,'е': 0.072,
    'ж': 0.007,'з': 0.016,'и': 0.062,'й': 0.010,'к': 0.028,'л': 0.035,
    'м': 0.026,'н': 0.053,'о': 0.090,'п': 0.023,'р': 0.040,'с': 0.045,
    'т': 0.053,'у': 0.021,'ф': 0.002,'х': 0.009,'ц': 0.003,'ч': 0.012,
    'ш': 0.006,'щ': 0.003,'ъ': 0.014,'ы': 0.016,'ь': 0.014,'э': 0.003,
    'ю': 0.006,'я': 0.018
}

ENG_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ENG_FREQ = {
    'e': 0.127,'t': 0.091,'a': 0.082,'o': 0.075,'i': 0.070,
    'n': 0.067,'s': 0.063,'h': 0.061,'r': 0.060,'d': 0.043,
    'l': 0.040,'c': 0.028,'u': 0.028,'m': 0.024,'w': 0.024,
    'f': 0.022,'g': 0.020,'y': 0.020,'p': 0.019,'b': 0.015,
    'v': 0.010,'k': 0.008,'x': 0.002,'j': 0.002,'q': 0.001,
    'z': 0.001
}

def normalize_text(text: str, alphabet: str) -> str:
    text = text.lower().replace('ё', 'е')
    return ''.join(c for c in text if c in alphabet)

def caesar_decrypt(text: str, shift: int, alphabet: str) -> str:
    result = []
    n = len(alphabet)
    for c in text:
        idx = alphabet.index(c)
        result.append(alphabet[(idx - shift) % n])
    return ''.join(result)

def letter_frequency(text: str, alphabet: str) -> dict:
    total = len(text)
    counter = Counter(text)
    return {char: counter.get(char, 0) / total for char in alphabet}

def least_squares_distance(freq1: dict, freq2: dict, alphabet: str) -> float:
    return sum((freq1.get(c, 0) - freq2.get(c, 0)) ** 2 for c in alphabet)

def break_for_alphabet(ciphertext, alphabet, ref_freq):
    text = normalize_text(ciphertext, alphabet)
    if not text:
        return None, float('inf'), ""

    best_shift = None
    best_score = float('inf')
    best_text = ""

    for shift in range(len(alphabet)):
        decrypted = caesar_decrypt(text, shift, alphabet)
        freq = letter_frequency(decrypted, alphabet)
        score = least_squares_distance(freq, ref_freq, alphabet)

        if score < best_score:
            best_score = score
            best_shift = shift
            best_text = decrypted

    return best_shift, best_score, best_text

def break_caesar_auto(ciphertext: str):
    text = ciphertext.lower().replace('ё', 'е')
    if any(c in RUS_ALPHABET for c in text):
        shift, score, decrypted = break_for_alphabet(ciphertext, RUS_ALPHABET, RUS_FREQ)
        return {
            "language": "ru",
            "shift": shift,
            "text": decrypted
        }
    else:
        shift, score, decrypted = break_for_alphabet(ciphertext, ENG_ALPHABET, ENG_FREQ)
        return {
            "language": "en",
            "shift": shift,
            "text": decrypted
        }

if __name__ == "__main__":
    cipher = """ФФФМ ЗГЬХ ЩЭЯГ ЪЖАГ ЧГВЪ ИЫЪА ЭЧГВ ЗГЗТ ЗГФЕ ХЬЧЪ БХБХ АУЦЭ АХЗХ ЯГШГ ЫЪАЗ
    ГЖЪЕ ГШГД ГАИЖ ЪЩГШ ГЭЧЖ ЪЬВХ УОЪШ ГЯХЯ ЬБЪФ ЕХЬЧ ЪБХА СМЭЯ ЧГЖЗ ХВЯЭ ВЪАЪ
    ЗГБЗ ХВЛЪ ЧХЧН ЭЮВХ ЩХМВ РКЦХ АХКТ ЗГФЗ ГЗЯЗ ГЯХЫ ЩРБГ ЗЧЪЗ ГБЫЪ АЗГЕ ГЗРБ
    ЧВИН ХЪЗД ГТЗХ БГЗЧ ЕХОЪ ВЭЪЬ АГЦИ ЭЖЗЕ ХКЕХ ЬЧЪЗ ГЗЯЗ ГЧДГ АВГМ ВРЪЖ ДГЕР
    ЧЖУБ ХАСМ ЭНЪМ СУЧЯ АХЩР ЧХАД ЕРЗС ТЗГФ ЗГЗЫ ЪЖХБ РЮЯГ ЗГЕР ЮВХЗ ЕХШЭ МЪЖЯ
    ЭЪЕХ ЬШГЧ ГЕРВ ХИМЭ АЖФБ ГАМХ ЗСЭН ИЗЭЗ СЧДЕ ГМЪБ ЗХЯЭ ЧЖЪШ ЩХВХ ЖЕЪЩ ЭВЪЕ
    ГЯГЧ ГШГЬ ЪБВГ ШГДИ ЗЭГЗ ВЭМЗ ГЫВГ ЮДЕЭ МЭВР ЯДЕЭ МЭВЪ ХШАФ ЩЭНС ЬХДА ИЗХА
    ЖФЧД ИЖЗР ВЪЭЖ ЧГЭК ЫЪЖА ЪЩГЧ ВЪВХ ЮЗЭЩ ХБЪВ ФВЪД ХВЗЪ ЕХДЕ РЫЯХ БЭВХ ДХЕЭ
    ЫЖЯЭ ЮМЪЕ ЩХЯЬ ХШВХ АХЭЧ ЪЕШЭ АЭФВ ЪЗЬХ ДАЪМ ХБЭЗ ГАСЯ ГЪЖЗ СГЩЭ ВГМЪ ЖЗЧГ
    ЧЕХБ ЪШГЧ ГЕФО ЪШГД ЕХЧЩ ИЖЗЪ ЯАХ"""
    result = break_caesar_auto(cipher)
    print(result)