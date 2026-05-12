from Decrypt import RUS_ALPHABET, ENG_ALPHABET, normalize_text

def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    
    text = normalize_text(text)

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

        shift_norm = shift % len(alphabet)
        idx = alphabet.index(char)
        new_char = alphabet[(idx + shift_norm) % len(alphabet)]

        result.append(new_char)
    return ''.join(result)
def caesar_reverse_encrypt(text: str, shift: int) -> str:
    
    text = normalize_text(text)

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

        shift_norm = shift % len(alphabet)
        idx = alphabet.index(char)
        new_char = alphabet[(idx - shift_norm) % len(alphabet)]

        result.append(new_char)

    return ''.join(result)

if __name__ == "__main__":
    print(caesar_encrypt("Привет, мир!", 3))

    print(caesar_encrypt("Hello, World!", 3))

    print(caesar_encrypt("Ёжик", 1))