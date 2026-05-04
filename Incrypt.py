from Decrypt import RUS_ALPHABET, ENG_ALPHABET

def normalize_shift(shift: int, alphabet_size: int) -> int:
    return shift % alphabet_size


def caesar_encrypt(text: str, shift: int) -> str:
    result = []

    for char in text:
        # Замена ё
        if char == 'ё':
            char = 'е'
        elif char == 'Ё':
            char = 'Е'

        # Кириллица
        if char.lower() in RUS_ALPHABET:
            alphabet = RUS_ALPHABET
        # Латиница
        elif char.lower() in ENG_ALPHABET:
            alphabet = ENG_ALPHABET
        else:
            result.append(char)
            continue

        is_upper = char.isupper()
        base_char = char.lower()

        shift_norm = normalize_shift(shift, len(alphabet))
        idx = alphabet.index(base_char)
        new_char = alphabet[(idx + shift_norm) % len(alphabet)]

        result.append(new_char.upper() if is_upper else new_char)

    return ''.join(result)

if __name__ == "__main__":
    print(caesar_encrypt("Привет, мир!", 3))

    print(caesar_encrypt("Hello, World!", 3))

    print(caesar_encrypt("Ёжик", 1))