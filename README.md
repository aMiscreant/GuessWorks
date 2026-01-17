<img width="340" height="340" alt="GuessWorks" src="https://github.com/user-attachments/assets/e1106fb7-f860-4d1b-8abc-0752e2e1fdf8" />

# Guess Works

+ `python3 guess_works.py`

### realistic password/wordlist generation

| Argument          | Description                                                                                                                   |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `-e, --essid`     | Target ESSID (e.g., BELL123456)                                                                                               |
| `-a, --area`      | Area code for phone number guesses (e.g., 416)                                                                                |
| `-s, --street`    | Street name (e.g., Main, KingWest)                                                                                            |
| `-o, --output`    | File to save the generated passwords                                                                                          |
| `--seasons`       | Include seasonal guesses                                                                                                      |
| `--months`        | Include month/year combinations                                                                                               |
| `--holidays`      | Include holiday-based guesses                                                                                                 |
| `--names`         | Include popular names + years                                                                                                 |
| `--events`        | Include global event-related patterns                                                                                         |
| `--sports`        | Include sports teams + years                                                                                                  |
| `--no-year`       | Exclude year suffix from guesses                                                                                              |
| `--add-numbers`   | Append numbers 1-N to each generated string (default 1–1000)                                                                  |
| `--clean-length`  | Remove lines under 8 characters long                                                                                          |
| `--clean-numbers` | Remove lines containing only numbers                                                                                          |
| `--capitalize`    | Capitalize the first character of each line (skips numbers)                                                                   |
| `--filler`        | Adds junk numeric strings to the start and end of file                                                                        |
| `--filler-count`  | Total filler lines (default: 7000, 5000 start + 2000 end)                                                                     |
| `--ai-names`      | Augments `--names` with offline AI-generated human names using a character-level Markov model trained on common name patterns |
| `--ai-ollama`     | Generate names or words using a local Ollama LLM. Uses a default `prompt.json` (editable) or a custom prompt via `--prompt`   |

---
+ ```bash
  # 1. Generate guesses for a specific ESSID
    python3 guess_works.py -e BELL123456 --seasons --holidays --output bell_guesses.txt

    # 2. Generate guesses based on a Canadian area code
    python3 guess_works.py -a 416 --add-numbers 50 --output phone_guesses.txt

    # 3. Generate guesses using street names and popular names
    python3 guess_works.py -s KingWest --names --no-year --output street_name_guesses.txt

    # 4. Generate guesses for sports teams and global events
    python3 guess_works.py --sports --events --capitalize --output event_sports_guesses.txt

    # 5. Generate a full mixed list with cleaning applied
    python3 guess_works.py -e VIRGIN123 --seasons --months --holidays --names --events --sports \
        --clean-length --clean-numbers --output full_wordlist.txt


---

# Pipe Wordlists Directly into Aircrack-ng

+ `gw_aircrack.py` generates enhanced password variants on-the-fly and can be piped straight into `aircrack-ng` without creating a large intermediate file.


| Flag          | Description                                     |
| ------------- | ----------------------------------------------- |
| `-i, --input` | Input wordlist file (required)                  |
| `--leet`      | Apply leetspeak substitutions                   |
| `--suffix`    | Append common suffixes (numbers, symbols, etc.) |
| `--prefix`    | Add common prefixes (`!`, `VIP`, etc.)          |
| `--toggle`    | Randomly toggle character case                  |
| `--max`       | Optional maximum number of variants to generate |
---
+ ```bash
    # 1. Generate with leetspeak + suffixes, pipe to aircrack-ng:
    python3 gw_aircrack.py -i base_words.txt --leet --suffix | aircrack-ng -w- -b <BSSID> capture.cap
    # 2. Apply all enhancements and limit to 50,000 variants:
    python3 gw_aircrack.py -i base_words.txt --leet --suffix --prefix --toggle --max 50000 | aircrack-ng -w- -b <BSSID> capture.cap
    # 3. Use without enhancements (just pass the base wordlist to aircrack-ng):
    python3 gw_aircrack.py -i base_words.txt | aircrack-ng -w- -b <BSSID> capture.cap


---

# Enhance Your Wordlist

+ `python3 gw_enhancer.py` applies leetspeak, prefixes, suffixes, and case toggling to an existing wordlist to generate realistic password variants.

#### Basic Usage

```bash
python3 gw_enhancer.py -i base_words.txt -o enhanced.txt --leet --suffix --prefix --toggle
```

| Flag           | Description                                                           |
| -------------- | --------------------------------------------------------------------- |
| `-i, --input`  | Input file with base words (required)                                 |
| `-o, --output` | Output file to save enhanced wordlist (required unless `--overwrite`) |
| `--leet`       | Apply leetspeak substitutions                                         |
| `--suffix`     | Append common suffixes (numbers, symbols, etc.)                       |
| `--prefix`     | Add common prefixes (`!`, `VIP`, etc.)                                |
| `--toggle`     | Randomly toggle character case for realism                            |
| `--overwrite`  | Overwrite input file instead of writing to output                     |
| `--max`        | Max number of generated variants (default very high)                  |

---
+ ```bash
    # 1. Enhance with leetspeak and suffixes:
    python3 gw_enhancer.py -i base_words.txt -o enhanced.txt --leet --suffix
    # 2. Add prefixes and toggle case:
    python3 gw_enhancer.py -i base_words.txt -o enhanced.txt --prefix --toggle
    # 3. Apply all enhancements:
    python3 gw_enhancer.py -i base_words.txt -o enhanced.txt --leet --suffix --prefix --toggle
    # 4. Overwrite the original wordlist:
    python3 gw_enhancer.py -i base_words.txt --overwrite --leet --suffix
    # 5. Limit output to 10,000 variants:
    python3 gw_enhancer.py -i base_words.txt -o enhanced.txt --leet --suffix --max 10000


---

# gw_merge

+ `python3 gw_merge.py`

### Merge and Clean Wordlists

This script combines all `.txt` files in the current directory, removes duplicates, sorts them, and saves the result to `wordlist_clean.txt`:

```bash
#!/usr/bin/env python3
import glob

output_file = "wordlist_clean.txt"
all_lines = set()

for filename in glob.glob("*.txt"):
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                all_lines.add(line)

with open(output_file, "w", encoding="utf-8") as f:
    for line in sorted(all_lines):
        f.write(line + "\n")

print(f"[+] Combined {len(all_lines)} unique lines into {output_file}")
```

---
