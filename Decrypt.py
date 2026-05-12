from collections import Counter

RUS_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
ENG_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

RUS_FREQ = {
    'а': 0.062, 'б': 0.014, 'в': 0.038, 'г': 0.013, 'д': 0.025,
    'е': 0.072, 'ж': 0.007, 'з': 0.016, 'и': 0.062, 'й': 0.010,
    'к': 0.028, 'л': 0.035, 'м': 0.026, 'н': 0.053, 'о': 0.090,
    'п': 0.023, 'р': 0.040, 'с': 0.045, 'т': 0.053, 'у': 0.021,
    'ф': 0.002, 'х': 0.009, 'ц': 0.003, 'ч': 0.012, 'ш': 0.006,
    'щ': 0.003, 'ъ': 0.014, 'ы': 0.016, 'ь': 0.014, 'э': 0.003,
    'ю': 0.006, 'я': 0.018
}

ENG_FREQ = {
    'e': 0.127, 't': 0.091, 'a': 0.082, 'o': 0.075, 'i': 0.070,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'r': 0.060, 'd': 0.043,
    'l': 0.040, 'c': 0.028, 'u': 0.028, 'm': 0.024, 'w': 0.024,
    'f': 0.022, 'g': 0.020, 'y': 0.020, 'p': 0.019, 'b': 0.015,
    'v': 0.010, 'k': 0.008, 'x': 0.002, 'j': 0.002, 'q': 0.001,
    'z': 0.001
}

# НОРМАЛИЗАЦИЯ

def normalize_text(text: str) -> str:

    text = text.lower().replace('ё', 'е')

    allowed = set(RUS_ALPHABET + ENG_ALPHABET)

    return ''.join(
        char for char in text
        if char in allowed
    )

# РАЗДЕЛЕНИЕ ТЕКСТА ПО ЯЗЫКАМ

def split_text_by_language(text: str) -> dict:

    text = normalize_text(text)

    ru_text = ''.join(c for c in text if c in RUS_ALPHABET)
    en_text = ''.join(c for c in text if c in ENG_ALPHABET)

    return {
        "ru": ru_text,
        "en": en_text
    }

# ЧАСТОТЫ БУКВ

def calculate_frequency(text: str, alphabet: str) -> dict:
    total = len(text)

    if total == 0:
        return {char: 0 for char in alphabet}

    counter = Counter(text)

    return {
        char: counter.get(char, 0) / total
        for char in alphabet
    }


# СДВИГ ТАБЛИЦЫ ЧАСТОТ

def shift_frequency_table(freq_table: dict, alphabet: str, shift: int) -> dict:

    n = len(alphabet)

    shifted = {}

    for i, char in enumerate(alphabet):
        shifted_char = alphabet[(i + shift) % n]
        shifted[shifted_char] = freq_table[char]

    return shifted

# РАССТОЯНИЕ МЕЖДУ ТАБЛИЦАМИ ЧАСТОТ

def frequency_distance(freq1: dict, freq2: dict, alphabet: str) -> float:
    return sum(
        (freq1[c] - freq2[c]) ** 2
        for c in alphabet
    )

# ПОИСК ЛУЧШЕГО СДВИГА ПО ЧАСТОТАМ

def find_best_shift(observed_freq: dict,
                    reference_freq: dict,
                    alphabet: str):

    best_shift = 0
    best_score = float('inf')

    for shift in range(len(alphabet)):

        shifted_reference = shift_frequency_table(
            reference_freq,
            alphabet,
            shift
        )

        score = frequency_distance(
            observed_freq,
            shifted_reference,
            alphabet
        )

        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift, best_score

# РАСШИФРОВКА

def caesar_decrypt(text: str,
                   shift: int,
                   alphabet: str) -> str:

    result = []

    n = len(alphabet)

    for char in text:

        if char.lower() not in alphabet:
            result.append(char)
            continue

        lower = char.lower()
        idx = alphabet.index(lower)

        decrypted = alphabet[(idx - shift) % n]

        if char.isupper():
            decrypted = decrypted.upper()

        result.append(decrypted)

    return ''.join(result)

# АВТОВЗЛОМ

def break_caesar_auto(ciphertext: str):

    normalized = normalize_text(ciphertext)

    separated = split_text_by_language(normalized)

    results = {}

    # Русский


    if separated["ru"]:

        ru_freq = calculate_frequency(
            separated["ru"],
            RUS_ALPHABET
        )

        ru_shift, ru_score = find_best_shift(
            ru_freq,
            RUS_FREQ,
            RUS_ALPHABET
        )

        results["ru"] = {
            "shift": ru_shift,
            "score": ru_score
        }

    # Английский

    if separated["en"]:

        en_freq = calculate_frequency(
            separated["en"],
            ENG_ALPHABET
        )

        en_shift, en_score = find_best_shift(
            en_freq,
            ENG_FREQ,
            ENG_ALPHABET
        )

        results["en"] = {
            "shift": en_shift,
            "score": en_score
        }

    # ОБЩИЙ СДВИГ

    if results['en']['score'] > results['ru']['score']:
        final_shift = results['en']['shift']
    else:
        final_shift = results['ru']['shift']


    # РАСШИФРОВКА ОБЩЕГО ТЕКСТА

    decrypted = []

    for char in normalized:

        lower = char.lower()

        if lower in RUS_ALPHABET:
            decrypted.append(
                caesar_decrypt(char, final_shift, RUS_ALPHABET)
            )

        elif lower in ENG_ALPHABET:
            decrypted.append(
                caesar_decrypt(char, final_shift, ENG_ALPHABET)
            )

        else:
            decrypted.append(char)

    return {
        "shift": final_shift,
        "languages_detected": list(results.keys()),
        "details": results,
        "text": ''.join(decrypted)
    }

if __name__ == "__main__":

    cipher = "lipps asvphуфмжй црмф" # helloworldприветмир

    result = break_caesar_auto(cipher)

    print("SHIFT:", result["shift"])
    print("LANGUAGES:", result["languages_detected"])
    print()
    print(result["text"])