from Decrypt import RUS_ALPHABET, ENG_ALPHABET

def normalize_shift(shift: int, alphabet_size: int) -> int:
    return shift % alphabet_size


def caesar_encrypt(text: str, shift: int) -> str:
    result = []

    for char in text:
        if char == 'ё' or char == 'Ё':
            char = 'е'

        char = char.lower()

        if char in RUS_ALPHABET:
            alphabet = RUS_ALPHABET
        elif char in ENG_ALPHABET:
            alphabet = ENG_ALPHABET
        else:
            result.append(char)
            continue

        shift_norm = normalize_shift(shift, len(alphabet))
        idx = alphabet.index(char)
        new_char = alphabet[(idx + shift_norm) % len(alphabet)]

        result.append(new_char)

    return ''.join(result)

if __name__ == "__main__":
    print(caesar_encrypt("Привет, мир!", 3))

    print(caesar_encrypt("Hello, World!", 3))

    print(caesar_encrypt("Ёжик", 1))