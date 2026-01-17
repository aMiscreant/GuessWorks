#!/usr/bin/env python3
# aMiscreant
import argparse
import json
import random
import string
import subprocess
from datetime import datetime

# Canadian phone prefixes, feel free to expand
area_codes = [
    '204', '226', '249', '289', '343', '365', '416', '437',
    '519', '548', '604', '613', '647', '705', '807', '905'
]

# Realistic seasonal/year combos
seasons = [
    # Standard seasons
    'winter', 'spring', 'summer', 'fall', 'autumn',
    'Winter', 'Spring', 'Summer', 'Fall', 'Autumn',
    'WINTER', 'SPRING', 'SUMMER', 'FALL', 'AUTUMN',

    # Abbreviations
    'win', 'spr', 'sum', 'fal', 'aut',
    'wn', 'sp', 'sm', 'fl', 'au',
    'wntr', 'sprng', 'smr', 'fl', 'autmn',

    # Weather types / patterns
    'rainy', 'dry', 'wet', 'monsoon', 'sunny', 'storm', 'stormy', 'fog', 'foggy',
    'hurricane', 'tornado', 'blizzard', 'frost', 'ice', 'hail', 'drought', 'typhoon', 'windy',
    'Rainy', 'Dry', 'Wet', 'Monsoon', 'Sunny', 'Storm', 'Stormy', 'Fog', 'Foggy',
    'Hurricane', 'Tornado', 'Blizzard', 'Frost', 'Ice', 'Hail', 'Drought', 'Typhoon', 'Windy',

    # Seasonal events / phenomena
    'snowfall', 'heatwave', 'coldfront', 'thaw', 'flood', 'avalanche', 'mudslide', 'coldwave', 'heatwave',
    'Snowfall', 'Heatwave', 'Coldfront', 'Thaw', 'Flood', 'Avalanche', 'Mudslide', 'Coldwave', 'Heatwave',

    # Seasonal astronomical markers
    'equinox', 'solstice', 'Equinox', 'Solstice',

    # Holidays that align with seasons
    'christmas', 'newyear', 'valentine', 'halloween', 'thanksgiving', 'easter',
    'Christmas', 'NewYear', 'Valentine', 'Halloween', 'Thanksgiving', 'Easter'
]


# Months
months = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Holidays (Capitalized and lowercase)
holidays = [
    # Christmas / New Year
    "christmas", "xmas", "newyear", "newyears", "nye",
    "Christmas", "Xmas", "NewYear", "NewYears", "NYE",
    "CHRISTMAS", "XMAS", "NEWYEAR", "NEWYEARS", "NYE",

    # Halloween / Thanksgiving / Easter
    "halloween", "hwn", "thanksgiving", "thanks", "easter", "eostre",
    "Halloween", "Hwn", "Thanksgiving", "Thanks", "Easter", "Eostre",
    "HALLOWEEN", "HWN", "THANKSGIVING", "THANKS", "EASTER", "EOSTRE",

    # Labour / Victoria / Canada Day / Boxing / Good Friday / Remembrance
    "labourday", "mayday", "canadaday", "victoriaday", "boxingday", "goodfriday",
    "LabourDay", "MayDay", "CanadaDay", "VictoriaDay", "BoxingDay", "GoodFriday",
    "LABOURDAY", "MAYDAY", "CANADADAY", "VICTORIADAY", "BOXINGDAY", "GOODFRIDAY",
    "remembranceday", "remday", "RemembranceDay", "RemDay", "REMEMBRANCEDAY", "REMDAY",

    # Religious / Cultural
    "valentines", "valentine", "hanukkah", "diwali", "eid", "ramadan", "kwanzaa", "holi", "thankas",
    "Valentines", "Valentine", "Hanukkah", "Diwali", "Eid", "Ramadan", "Kwanzaa", "Holi", "ThankAs",
    "VALENTINES", "VALENTINE", "HANUKKAH", "DIWALI", "EID", "RAMADAN", "KWANZAA", "HOLI", "THANKAS",

    # International / Fun holidays
    "aprilfools", "pieday", "stpatricks", "stpatrick", "halloweenparty", "newyearsday",
    "AprilFools", "PieDay", "StPatricks", "StPatrick", "HalloweenParty", "NewYearsDay",
    "APRILFOOLS", "PIEDAY", "STPATRICKS", "STPATRICK", "HALLOWEENPARTY", "NEWYEARSDAY"
]

popular_names = [
    # Male (Capitalized)
    "James", "Michael", "John", "Robert", "David", "William", "Richard", "Joseph", "Thomas", "Christopher",
    "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Steven", "Donald", "Andrew", "Joshua", "Paul",
    "Kenneth", "Kevin", "Brian", "Timothy", "Ronald", "Jason", "George", "Edward", "Jeffrey", "Ryan",
    "Jacob", "Nicholas", "Gary", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Benjamin", "Scott",
    "Brandon", "Samuel", "Gregory", "Alexander", "Patrick", "Frank", "Jack", "Raymond", "Dennis", "Tyler",
    "Aaron", "Jerry", "Jose", "Nathan", "Adam", "Henry", "Zachary", "Douglas", "Peter", "Noah",
    "Kyle", "Ethan", "Christian", "Jeremy", "Keith", "Austin", "Sean", "Roger", "Terry", "Walter",
    "Dylan", "Gerald", "Carl", "Jordan", "Bryan", "Gabriel", "Jesse", "Harold", "Lawrence", "Logan",
    "Arthur", "Bruce", "Billy", "Elijah", "Joe", "Alan", "Juan", "Liam", "Willie", "Mason",
    "Albert", "Randy", "Wayne", "Vincent", "Lucas", "Caleb", "Luke", "Bobby", "Isaac", "Bradley",

    # Female (Capitalized)
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Karen", "Sarah",
    "Lisa", "Nancy", "Sandra", "Ashley", "Emily", "Kimberly", "Betty", "Margaret", "Donna", "Michelle",
    "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Amy",
    "Kathleen", "Angela", "Dorothy", "Shirley", "Emma", "Brenda", "Nicole", "Pamela", "Samantha", "Anna",
    "Katherine", "Christine", "Debra", "Rachel", "Olivia", "Carolyn", "Maria", "Janet", "Heather", "Diane",
    "Catherine", "Julie", "Victoria", "Helen", "Joyce", "Lauren", "Kelly", "Christina", "Joan", "Judith",
    "Ruth", "Hannah", "Evelyn", "Andrea", "Virginia", "Megan", "Cheryl", "Jacqueline", "Madison", "Sophia",
    "Abigail", "Teresa", "Isabella", "Sara", "Janice", "Martha", "Gloria", "Kathryn", "Ann", "Charlotte",
    "Judy", "Amber", "Julia", "Grace", "Denise", "Danielle", "Natalie", "Alice", "Marilyn", "Diana",
    "Beverly", "Jean", "Brittany", "Theresa", "Frances", "Kayla", "Alexis", "Tiffany", "Lori", "Kathy",

    # Male (lowercase)
    "james", "michael", "john", "robert", "david", "william", "richard", "joseph", "thomas", "christopher",
    "charles", "daniel", "matthew", "anthony", "mark", "steven", "donald", "andrew", "joshua", "paul",
    "kenneth", "kevin", "brian", "timothy", "ronald", "jason", "george", "edward", "jeffrey", "ryan",
    "jacob", "nicholas", "gary", "eric", "jonathan", "stephen", "larry", "justin", "benjamin", "scott",
    "brandon", "samuel", "gregory", "alexander", "patrick", "frank", "jack", "raymond", "dennis", "tyler",
    "aaron", "jerry", "jose", "nathan", "adam", "henry", "zachary", "douglas", "peter", "noah",
    "kyle", "ethan", "christian", "jeremy", "keith", "austin", "sean", "roger", "terry", "walter",
    "dylan", "gerald", "carl", "jordan", "bryan", "gabriel", "jesse", "harold", "lawrence", "logan",
    "arthur", "bruce", "billy", "elijah", "joe", "alan", "juan", "liam", "willie", "mason",
    "albert", "randy", "wayne", "vincent", "lucas", "caleb", "luke", "bobby", "isaac", "bradley",

    # Female (lowercase)
    "mary", "patricia", "jennifer", "linda", "elizabeth", "barbara", "susan", "jessica", "karen", "sarah",
    "lisa", "nancy", "sandra", "ashley", "emily", "kimberly", "betty", "margaret", "donna", "michelle",
    "carol", "amanda", "melissa", "deborah", "stephanie", "rebecca", "sharon", "laura", "cynthia", "amy",
    "kathleen", "angela", "dorothy", "shirley", "emma", "brenda", "nicole", "pamela", "samantha", "anna",
    "katherine", "christine", "debra", "rachel", "olivia", "carolyn", "maria", "janet", "heather", "diane",
    "catherine", "julie", "victoria", "helen", "joyce", "lauren", "kelly", "christina", "joan", "judith",
    "ruth", "hannah", "evelyn", "andrea", "virginia", "megan", "cheryl", "jacqueline", "madison", "sophia",
    "abigail", "teresa", "isabella", "sara", "janice", "martha", "gloria", "kathryn", "ann", "charlotte",
    "judy", "amber", "julia", "grace", "denise", "danielle", "natalie", "alice", "marilyn", "diana",
    "beverly", "jean", "brittany", "theresa", "frances", "kayla", "alexis", "tiffany", "lori", "kathy"
]

popular_names += [name.lower() for name in popular_names if name[0].isupper()]

# Special global events (password themes people often use)
special_events = [
    # Pandemics / health
    "covid", "pandemic", "quarantine", "lockdown", "coronavirus", "vaccine",
    "COVID", "Pandemic", "Quarantine", "Lockdown", "Coronavirus", "Vaccine",

    # Sports / global events
    "worldcup", "olympics", "fifa", "FIFA", "superbowl", "SuperBowl", "nba", "NFL", "WWDC", "CES",
    "Eurovision", "Grammys", "Oscars", "olympic", "WorldCup", "Olympics", "NBA", "Nfl",

    # Politics / global figures
    "election", "Trump", "Biden", "Putin", "Obama", "Macron", "Merkel", "XiJinping",
    "Election", "trump", "biden", "putin", "obama", "macron", "merkel", "XiJinping",

    # Tech / crypto / internet culture
    "metaverse", "elonmusk", "moonlanding", "coldwar", "bitcoin", "ethereum", "dogecoin", "NFT",
    "Metaverse", "ElonMusk", "MoonLanding", "ColdWar", "Bitcoin", "Ethereum", "Dogecoin", "NFT",

    # TV / movies / pop culture
    "gameofthrones", "got", "strangerthings", "starwars", "marvel", "dccomics", "harrypotter", "lotr",
    "GameofThrones", "GOT", "StrangerThings", "StarWars", "Marvel", "DCComics", "HarryPotter", "LOTR",

    # Misc major events
    "brexit", "greta", "climatechange", "flood", "wildfire", "typhoon", "hurricane",
    "Brexit", "Greta", "ClimateChange", "Flood", "Wildfire", "Typhoon", "Hurricane"
]

sport_teams_hockey = [
    # Lowercase
    "canadiens", "mapleleafs", "bruins", "rangers", "islanders", "flyers", "penguins", "capitals",
    "hurricanes", "panthers", "lightning", "senators", "sabres", "redwings", "bluejackets", "devils",
    "blackhawks", "wild", "predators", "blues", "avalanche", "stars", "jets", "coyotes",
    "ducks", "kings", "sharks", "flames", "oilers", "kraken", "goldenknights", "canucks",

    # Capitalized
    "Canadiens", "MapleLeafs", "Bruins", "Rangers", "Islanders", "Flyers", "Penguins", "Capitals",
    "Hurricanes", "Panthers", "Lightning", "Senators", "Sabres", "RedWings", "BlueJackets", "Devils",
    "Blackhawks", "Wild", "Predators", "Blues", "Avalanche", "Stars", "Jets", "Coyotes",
    "Ducks", "Kings", "Sharks", "Flames", "Oilers", "Kraken", "GoldenKnights", "Canucks"
]

# Official NHL teams (full names)
nhl_teams = [
    "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames",
    "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets",
    "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings",
    "Minnesota Wild", "Montreal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders",
    "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks",
    "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks",
    "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"
]

# Generate lowercase and capitalized forms automatically
sport_teams_hockey = []
for team in nhl_teams:
    sport_teams_hockey.append(team.lower().replace(" ", ""))   # lowercase, no spaces
    sport_teams_hockey.append(team.title().replace(" ", ""))   # capitalized, no spaces

# Full NFL team names
nfl_teams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# Common nicknames / abbreviations
nfl_abbr = [
    "Cards", "Fins", "Pats", "Jets", "Bucs", "Skins", "Chiefs", "Packers",
    "Ravens", "Steelers", "Bears", "Lions", "Cowboys", "Giants", "Rams", "Chargers",
    "Falcons", "Panthers", "Seahawks", "49ers", "Texans", "Broncos", "Dolphins",
    "Titans", "Raiders", "Saints", "Eagles", "Bengals", "Browns", "Commanders"
]

# Generate lowercase and capitalized versions
sport_teams_football = []

for team in nfl_teams + nfl_abbr:
    name_clean = team.replace(" ", "").replace("-", "").lower()
    sport_teams_football.append(name_clean)
    sport_teams_football.append(name_clean.title())


# Full NBA teams
nba_teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards"
]

# Common nicknames / abbreviations
nba_abbr = [
    "Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavs", "Mavs", "Nuggets",
    "Pistons", "Warriors", "Rockets", "Pacers", "Clippers", "Lakers", "Grizzlies", "Heat",
    "Bucks", "Timberwolves", "Pelicans", "Knicks", "Thunder", "Magic", "Sixers", "Suns",
    "Blazers", "Kings", "Spurs", "Raptors", "Jazz", "Wizards"
]

# Generate lowercase and capitalized versions
sport_teams_basketball = []

for team in nba_teams + nba_abbr:
    name_clean = team.replace(" ", "").replace("-", "").lower()
    sport_teams_basketball.append(name_clean)
    sport_teams_basketball.append(name_clean.title())


years = [str(y) for y in range(datetime.now().year - 125, datetime.now().year + 1)]

# --- Guess Generators ---
def isp_default_guesses(essid):
    essid = essid.upper()
    guesses = []
    if essid.startswith("BELL"):
        base = essid.replace("BELL", "")
        if base.isdigit():
            guesses += [f"{p}{base}" for p in ["BELL", "bell", "Bell"]]
    elif essid.startswith("VIRGIN"):
        base = essid.replace("VIRGIN", "")
        guesses += [f"{p}{base}pass" for p in ["virgin", "VIRGIN"]]
    elif "ROGERS" in essid:
        base = essid.split("ROGERS")[-1]
        if base.isdigit():
            guesses += [f"{p}{base}" for p in ["ROGERS", "rogers", "Rogers"]]
        guesses += ["rogers1234", "rogerswifi"]

    guesses += [essid.lower() + s for s in ["123", "2024", "!@#"]]
    return guesses


def process_wordlist(guesses, args):
    processed = []

    for line in guesses:
        # Remove lines under 8 characters
        if args.clean_length and len(line) < 8:
            continue
        # Remove lines with only numbers
        if args.clean_numbers and line.isdigit():
            continue
        # Capitalize first character (skip numbers)
        if args.capitalize and not line[0].isdigit():
            line = line[0].upper() + line[1:]

        processed.append(line)

    return processed


def phone_number_guesses(area):
    for i in range(0, 1000000):
        yield f"{area}{i:07d}"  # zero-padded to 7 digits

def street_guesses(street):
    return [f"{street.lower()}{i}" for i in range(1, 1001)]


def season_guesses(args):
    if args.add_numbers:
        return [f"{s}{i}" for s in seasons for i in range(1, args.add_numbers + 1)]
    return [f"{s}{y}" if not args.no_year else s for s in seasons for y in years]

def month_guesses(args):
    if args.add_numbers:
        return [f"{m}{i}" for m in months for i in range(1, args.add_numbers + 1)]
    return [f"{m}{y}" if not args.no_year else m for m in months for y in years]

def holiday_guesses(args):
    if args.add_numbers:
        return [f"{h}{i}" for h in holidays for i in range(1, args.add_numbers + 1)]
    return [f"{h}{y}" if not args.no_year else h for h in holidays for y in years]

def name_guesses(args):
    base_names = popular_names.copy()
    if args.ai_names:
        base_names += ai_markov_names(popular_names, count=300)
    if args.add_numbers:
        return [f"{name}{i}" for name in base_names for i in range(1, args.add_numbers + 1)]
    return [f"{name}" if args.no_year else f"{name}{y}" for name in base_names for y in years]

def event_guesses(args):
    if args.add_numbers:
        return [f"{event}{i}" for event in special_events for i in range(1, args.add_numbers + 1)]
    return [f"{event}{y}" if not args.no_year else event for event in special_events for y in years]

def sports_guesses(args):
    all_teams = sport_teams_hockey + sport_teams_football + sport_teams_basketball
    if args.add_numbers:
        return [f"{team}{i}" for team in all_teams for i in range(1, args.add_numbers + 1)]
    return [f"{team}{y}" if not args.no_year else team for team in all_teams for y in years]

def random_filler_lines(count=1000, length=8):
    """Generate N random numeric strings of given length."""
    return ["".join(random.choices(string.digits, k=length)) for _ in range(count)]

def ai_ollama_generate(args, default_prompt_file="prompt.json"):
    """
    Generate wordlist components using a local Ollama LLM.
    Returns a list of strings (one per line).
    """
    # Build final prompt
    if args.prompt:
        user_prompt = args.prompt
    else:
        try:
            with open(default_prompt_file, "r") as f:
                prompt_json = json.load(f)
        except FileNotFoundError:
            print("[!] prompt.json not found and no --prompt provided")
            return []

        # Wrap JSON into an instruction the model understands
        user_prompt = (
            "Generate realistic password components.\n"
            "Output ONLY raw words or names, one per line.\n"
            "No explanations, no numbering, no symbols.\n\n"
            f"Context:\n{json.dumps(prompt_json, indent=2)}"
        )

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=user_prompt,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("[!] Ollama execution failed")
        print(e.stderr)
        return []

    words = []
    for line in result.stdout.splitlines():
        line = line.strip()
        # Clean common LLM formatting
        line = line.lstrip("-•0123456789. ").strip()
        if not line:
            continue
        if len(line) < 3:
            continue
        if " " in line:
            continue

        words.append(line)

    return words

# --- Master Guess Generator ---
def generate_guesses(args):
    all_guesses = set()

    if args.essid:
        all_guesses.update(isp_default_guesses(args.essid))
    if args.area:
        all_guesses.update(phone_number_guesses(args.area))
    if args.street:
        all_guesses.update(street_guesses(args.street))
    if args.seasons:
        all_guesses.update(season_guesses(args))
    if args.months:
        all_guesses.update(month_guesses(args))
    if args.holidays:
        all_guesses.update(holiday_guesses(args))
    if args.names:
        all_guesses.update(name_guesses(args))
    if args.events:
        all_guesses.update(event_guesses(args))
    if args.sports:
        all_guesses.update(sports_guesses(args))
    if args.ai_ollama:
        all_guesses.update(ai_ollama_generate(args))

    return sorted(all_guesses)

def ai_markov_names(seed_names, count=200, min_len=4, max_len=10):
    """
    Simple character-level Markov chain name generator
    """
    from collections import defaultdict
    chains = defaultdict(list)

    for name in seed_names:
        name = f"^{name.lower()}$"
        for i in range(len(name) - 2):
            chains[name[i:i+2]].append(name[i+2])

    generated = set()

    while len(generated) < count:
        key = "^" + random.choice(string.ascii_lowercase)
        name = ""
        while True:
            next_chars = chains.get(key)
            if not next_chars:
                break
            c = random.choice(next_chars)
            if c == "$":
                break
            name += c
            key = key[1] + c

        if min_len <= len(name) <= max_len:
            generated.add(name)

    return list(generated)


# --- CLI ---
def main():
    # python3 password_list_generator.py --names
    parser = argparse.ArgumentParser(description="Real-life password list generator for Wi-Fi cracking.")
    parser.add_argument("-e", "--essid",
                        help="Target ESSID (e.g. BELL123456)")
    parser.add_argument("-a", "--area",
                        help="Area code (e.g. 416)")
    parser.add_argument("-s", "--street",
                        help="Street name (e.g. Main, KingWest)")
    parser.add_argument("-o", "--output",
                        help="Save to file")

    # New argument switches
    parser.add_argument("--seasons", action="store_true",
                        help="Include seasonal guesses")
    parser.add_argument("--months", action="store_true",
                        help="Include month/year combinations")
    parser.add_argument("--holidays", action="store_true",
                        help="Include holiday-based guesses")
    parser.add_argument("--names", action="store_true",
                        help="Include popular names + years")
    parser.add_argument("--events", action="store_true",
                        help="Include global event-related patterns")
    parser.add_argument("--sports", action="store_true",
                        help="Include sports teams + years")

    # Global flag to exclude years
    parser.add_argument("--no-year", action="store_true",
                        help="Exclude year suffix from guesses")
    parser.add_argument("--add-numbers", type=int, nargs='?', const=1000,
                        help="Append numbers 1-N to each generated string (default 1-1000)")

    # Wordlist cleaners
    parser.add_argument("--clean-length", action="store_true",
                        help="Remove lines under 8 characters long")
    parser.add_argument("--clean-numbers", action="store_true",
                        help="Remove lines that contain only numbers")
    parser.add_argument("--capitalize", action="store_true",
                        help="Capitalize the first character of each line (skips lines starting with numbers)")

    # New switch for filler
    parser.add_argument("--filler", action="store_true",
                        help="Add 8000 random numeric 8-char strings at start and end")
    parser.add_argument("--filler-count", type=int, default=7000,
                        help="Total filler lines (default: 7000, 5000 start + 2000 end)")

    # AI integration
    parser.add_argument("--ai-names", action="store_true",
        help="Augment --names with offline AI-generated human names (Markov-based)")
    parser.add_argument("--ai-ollama", action="store_true",
        help="Generate names or words using a local Ollama LLM (uses prompt.json by default)")
    parser.add_argument("--prompt", type=str,
        help="Manual prompt string for --ai-ollama (overrides prompt.json)")

    args = parser.parse_args()

    if args.ai_names:
        args.names = True

    if args.prompt and not args.ai_ollama:
        parser.error("--prompt requires --ai-ollama")

    guesses = generate_guesses(args)
    guesses = process_wordlist(guesses, args)

    if args.filler:
        # Default split: 5000 front, rest at end
        front = 5000 if args.filler_count > 5000 else args.filler_count
        back = max(0, args.filler_count - front)
        fillers_front = random_filler_lines(front, 8)
        fillers_back = random_filler_lines(back, 8)
        guesses = fillers_front + guesses + fillers_back

    if args.output:
        with open(args.output, 'w') as f:
            for pw in guesses:
                f.write(pw + "\n")
        print(f"[+] Saved {len(guesses)} passwords to {args.output}")
    else:
        print("\n[+] Generated Guesses:")
        for pw in guesses:
            print(f" → {pw}")
        print(f"\n[✓] Total: {len(guesses)} guesses")


if __name__ == "__main__":
    main()