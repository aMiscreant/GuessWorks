#!/usr/bin/env python3
# aMiscreant
import argparse
import itertools
import random
import string

LEET_MAP = {
    'a': ['4', '@', '^', 'à', 'æ'],
    'b': ['8', 'ß'],
    'c': ['(', '<', '¢'],
    'e': ['3', '€'],
    'g': ['9', '6'],
    'h': ['#'],
    'i': ['1', '!', '|', 'ï'],
    'l': ['1', '|', '£'],
    'o': ['0', '()', '*'],
    's': ['5', '$', '§'],
    't': ['7', '+'],
    'z': ['2'],
    'x': ['%'],
    'q': ['9']
}

# ToDo 1-10 combos
SUFFIXES = [
    '123', '1234', '12345',
    '!', '@', '#', '$', '!!',
    '2023', '2024', '2025',
    '1!', '12', '!@#', '321',
    '007', '911', '666', '420', '69',
    'abc', 'xyz', 'qwe', 'asd',
    'pass', 'pwd', 'pw',
    'love', 'hate', 'god', 'life',
    'CAN', 'USA', 'ONT', 'TO',
    '!', '!1', '1!', '!!',
    '?', '??', '!?', '*'
]

PREFIXES = [
    '!', '@', '#', '$', '2024', 'VIP', 'the', 'mr', 'ms', 'dr'
]

MAX_LEET_REPLACEMENTS = 1  # Max chars replaced per word to avoid explosion


def load_words(file):
    with open(file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def toggle_case(word):
    # Randomly toggle some characters case for realism
    new_word = []
    for ch in word:
        if ch.isalpha() and random.random() < 0.5:
            new_word.append(ch.upper() if ch.islower() else ch.lower())
        else:
            new_word.append(ch)
    return ''.join(new_word)


def generate_ios_password(length=20):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(random.choices(chars, k=length))

def generate_android_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#"
    return ''.join(random.choices(chars, k=length))

def generate_memorable_password():
    words = ['sun', 'moon', 'star', 'cloud', 'river', 'wolf', 'cat', 'blue', 'fire', 'tree']
    return random.choice(words).capitalize() + str(random.randint(10, 99)) + random.choice('!@#')


def leetspeak_variants(word):
    # Find all positions where leet substitutions can happen
    positions = []
    for ch in word:
        lower = ch.lower()
        if lower in LEET_MAP:
            replacements = LEET_MAP[lower]
            # Original char + replacements
            positions.append([ch] + replacements)
        else:
            positions.append([ch])

    # To limit explosion, randomly select up to MAX_LEET_REPLACEMENTS positions to replace
    replace_positions = [i for i, chars in enumerate(positions) if len(chars) > 1]
    if len(replace_positions) > MAX_LEET_REPLACEMENTS:
        replace_positions = random.sample(replace_positions, MAX_LEET_REPLACEMENTS)

    def gen_replacements():
        for combo in itertools.product(*[
            positions[i] if i not in replace_positions else positions[i][1:]
            for i in range(len(positions))
        ]):
            yield ''.join(combo)

    # Always include the original word
    variants = set([word])
    variants.update(gen_replacements())
    return variants


def apply_suffixes(words):
    for word in words:
        for suffix in SUFFIXES:
            yield word + suffix


def apply_prefixes(words):
    for word in words:
        for prefix in PREFIXES:
            yield prefix + word


def generate_variants(words, do_leet, do_suffix, do_prefix, do_toggle):
    variants = set(words)

    if do_leet:
        leet_expanded = set()
        for w in variants:
            leet_expanded.update(leetspeak_variants(w))
        variants = leet_expanded

    if do_toggle:
        toggle_expanded = set()
        for w in variants:
            toggle_expanded.add(toggle_case(w))
        variants.update(toggle_expanded)

    if do_prefix:
        variants.update(apply_prefixes(variants))

    if do_suffix:
        variants.update(apply_suffixes(variants))

    return variants


def main():
    # python3 enhance_wordlist.py -i base_words.txt -o enhanced.txt --leet --suffix --prefix --toggle --max 10000
    parser = argparse.ArgumentParser(description="Advanced wordlist enhancer with leetspeak, suffixes, prefixes, toggle case.")
    parser.add_argument("-i", "--input", required=True, help="Input file with words")
    parser.add_argument("-o", "--output", required=True, help="Output file to write enhanced words")
    parser.add_argument("--leet", action="store_true", help="Apply leetspeak substitutions")
    parser.add_argument("--suffix", action="store_true", help="Append common suffixes")
    parser.add_argument("--prefix", action="store_true", help="Add common prefixes")
    parser.add_argument("--toggle", action="store_true", help="Randomly toggle case in words")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite input file instead of writing to output")
    parser.add_argument("--max", type=int, default=5000000000000, help="Max number of generated variants (to avoid huge output)")

    args = parser.parse_args()

    words = load_words(args.input)

    variants = generate_variants(
        words,
        do_leet=args.leet,
        do_suffix=args.suffix,
        do_prefix=args.prefix,
        do_toggle=args.toggle,
    )

    # Limit output size
    if len(variants) > args.max:
        print(f"[!] Variant count ({len(variants)}) exceeds max ({args.max}), sampling down...")
        variants = set(random.sample(variants, args.max))

    target_file = args.input if args.overwrite else args.output
    with open(target_file, 'w', encoding='utf-8') as f:
        for word in sorted(variants):
            f.write(word + '\n')

    print(f"[✓] Enhanced list saved to {target_file} ({len(variants)} entries)")


if __name__ == "__main__":
    main()
