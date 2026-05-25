import re
import os
import json
from typing import Any
from rich.console import Console

console = Console(highlight=False)


######################### CONSTANT VALUES #########################


# Line colours. Enhanced are more accurate to official PTV branding whereas native uses the terminal's defined colours instead.
COLOUR_STORE: dict[str, dict[str, str]] = {
    'enhanced': {
        # Group/line colours
        'Alamein': '#F2F2F2 on #094c8d',
        'Belgrave': '#F2F2F2 on #094c8d',
        'Glen Waverley': '#F2F2F2 on #094c8d',
        'Lilydale': '#F2F2F2 on #094c8d',
        'Cranbourne': '#0C0C0C on #16b4e8',
        'Pakenham': '#0C0C0C on #16b4e8',
        'Hurstbridge': '#F2F2F2 on #b1211b',
        'Mernda': '#F2F2F2 on #b1211b',
        'Craigieburn': 'black on #ffb531',
        'Sunbury': '#0C0C0C on #ffb531',
        'Upfield': '#0C0C0C on #ffb531',
        'Flemington Racecourse': '#0C0C0C on #909295',
        'Frankston': '#F2F2F2 on #159943',
        'Stony Point': '#F2F2F2 on #159943',
        'Werribee': '#F2F2F2 on #159943',
        'Williamstown': '#F2F2F2 on #159943',
        'Sandringham': '#0C0C0C on #fc7fbb',
    },
    'native': {
        # Line colours
        'Alamein': 'black on bright_blue',
        'Belgrave': 'black on bright_blue',
        'Glen Waverley': 'black on bright_blue',
        'Lilydale': 'black on bright_blue',
        'Cranbourne': 'black on bright_cyan',
        'Pakenham': 'black on bright_cyan',
        'Hurstbridge': 'black on bright_red',
        'Mernda': 'black on bright_red',
        'Craigieburn': 'black on bright_yellow',
        'Sunbury': 'black on bright_yellow',
        'Upfield': 'black on bright_yellow',
        'Flemington Racecourse': 'black on white',
        'Frankston': 'black on green',
        'Stony Point': 'black on green',
        'Werribee': 'black on green',
        'Williamstown': 'black on green',
        'Sandringham': 'black on bright_magenta',
    },
}

# Dict to convert avg travel time stored as an integer in datastore.json into a human-readable format
INT_TO_TIMERANGE: dict[int, str] = {
    0: 'under 10',
    1: '11 to 20',
    2: '21 to 30',
    3: '31 to 40',
    4: '41 to 50',
    5: '51 to 60',
    6: '61 to 70',
    7: '71 to 80',
    8: '81 to 90',
    9: '91 to 100',
    10: '101 to 110',
}

# Dict containing each group and what lines are apart of it
LINE_GROUPS: dict[str, list[str]] = {
    'Burnley': ['Alamein', 'Belgrave', 'Glen Waverley', 'Lilydale'],
    'Caufield': ['Cranbourne', 'Pakenham'],
    'Clifton Hill': ['Hurstbridge', 'Mernda'],
    'Northern': ['Craigieburn', 'Sunbury', 'Upfield'],
    'Cross City': ['Frankston', 'Werribee', 'Williamstown'],
}

# Dict containing info regarding city loop operations
CITY_LOOP_INFO: dict[str, str] = {
    'Burnley': 'Burnley group services travel anti-clockwise through the city loop on weekday mornings, clockwise on weekday afternoons and weekends.',
    'Caufield': 'Caufield group services travel anti-clockwise through the city loop.',
    'Clifton Hill': 'Clifton Hill group services travel clockwise through the city loop.',
    'Northern': 'Northern group services travel clockwise through the city loop on weekday mornings and weekends, anti-clockwise on weekday afternoons.',
}

# Dict containing info that applies to each station on a line
MISC_LINE_INFO: dict[str, str] = {
    'Alamein': 'Services on the Alamein line operate as a shuttle to Camperwell Station outside of weekday peaks.',
    'Frankston': 'Frankston line up services may through-run with the Werribee and Williamstown lines.',
    'Werribee': 'Werribee line up services may through-run with the Frankston line.',
    'Williamstown': 'Williamstown line up services may through-run with the Frankston line.',
}

# Dict containiong lists of stations that have conflicting misc info so they can be ignored when shown to the user
MISC_LINE_INFO_CONFLICTS: list[list[str]] = [
    ['Frankston', 'Werribee', 'Williamstown'],
]


######################### CORE FUNCTIONS #########################


# Runs OS-specific shell command to clear console
def clear() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Load saved, visited and unvisited stations from datastore.json, which should be in the same directory.
def read() -> dict[str, Any]:
    # Displays an error if datastore.json is not found in the current working directory rather than crashing outright
    try:
        with open('./data/datastore.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(
            'Could not find datastore.json. This file is required for Railway Roulette to run and must be in the same folder as the program.\n\nIf you need a new copy of this file, you can download it here: https://github.com/mudkipscience/rail_roulette/blob/main/src/datastore.json\n'
        )
        input('Press enter to exit.')

        exit()


# Write modified .json to datastore.json
def write(data: dict[str, Any]) -> None:
    with open('./data/datastore.json', 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


# Generates a string of options the user can select from. ops is an array of names we want to give to each option.
def print_menu(ops: list[str]) -> None:
    menu: str = ''

    for i, entry in enumerate(ops, 1):
        menu += f'{i}) {entry}\n'

    print(menu)


def get_colours(data: dict[str, Any]) -> dict[str, str]:
    if data['config']['use_enhanced_colours'] is True:
        return COLOUR_STORE['enhanced']
    else:
        return COLOUR_STORE['native']


# (for now) this function only searches stations based on a partial string (e.g. "fli" will return Flinders Street, "fern" will return Ferntree Gully and Upper Ferntree Gully, "so cro" will return Southern Cross)
def fuzzy_search(data: dict[str, Any], include_visited: bool = False) -> str | None:
    # Use a set to prevent duplicates
    results: set[str] = set()

    # Use a nested function to save me writing almost the same code twice - returns none as this mutates the existing variable results which is accessible from this scope
    def find_results(stations: list[str]) -> None:
        for stn in stations:
            # Basic stuff, if the query (substring) is found to be in the station name, add that station name to the results set
            if query in stn.lower():
                results.add(stn)

        # Does the same thing as above but only if include_visited is True
        if include_visited is True:
            visited_stns = list(data['visited'].keys())
            for stn in visited_stns:
                if query in stn.lower():
                    results.add(stn)

        # Split the words in the query at whitespace (fli st becomes ['fli', st'])
        split_query: list[str] = query.split()

        if len(split_query) > 1:
            for stn in stations:
                matches_found: int = 0

                # Try and match each split query against a station name
                for substr in split_query:
                    if substr in stn.lower():
                        matches_found += 1

                # if matches_found == the length of the split_query list, a match must have been found
                if matches_found == len(split_query):
                    results.add(stn)

    while True:
        query: str = input('> ').lower()

        if len(query) == 0:
            break

        find_results(list(data['unvisited'].keys()))

        if include_visited is True:
            find_results(list(data['visited'].keys()))

        search: list[str] = sorted(list(results))

        if len(search) == 0:
            print('\nStation not found, recheck spelling.\n')
        elif len(search) > 5:
            print('\nToo many results, try another query.\n')
            results.clear()
        else:
            if len(search) > 1:
                console.print(
                    '\nFound multiple stations, please select one from the options below:\n'
                )

                print_menu(search + ['Return to main menu'])
                while True:
                    choice: str | int = input('> ')

                    if not choice.isdigit():
                        print('\nError: Input must be a valid whole number.\n')
                    else:
                        choice = int(choice) - 1

                        if choice < 0 or choice > len(search):
                            print(
                                f'\nError: Input must be between 1 and {len(search) + 1}\n'
                            )
                        elif choice == len(search):
                            return
                        else:
                            return search[choice]
            else:
                return search[0]


# Asks for a date from the user, checks to make sure it is valid and formatted as DD/MM/YYYY then returns it
def assign_date(stn_name: str) -> str | None:
    # Regular expression that checks for a valid DD/MM/YYYY format (I don't think I need to worry about MM/DD/YYYY freaks given this is a Melbourne-specific program)
    regex: str = '(0[1-9]|[12][0-9]|3[01])\\/(0[1-9]|1[0,1,2])\\/(20)\\d{2}'

    print(
        f'\nType in the date you visited {stn_name} in the format of DD/MM/YYYY below, or type "skip" to skip.\n'
    )

    while True:
        user_input: str = input('> ')

        if user_input == 'skip':
            break

        # Check to make sure the length is valid before running regex checks
        elif len(user_input) != 10:
            print(
                '\nInvalid choice. Please either enter a date in the format of DD/MM/YYYY or type "skip".\n'
            )

        else:
            # Use regex to validate the user input
            date: re.Match[str] | None = re.search(regex, user_input)

            if date:
                return user_input
            else:
                print(
                    '\nInvalid date. Please enter a date in the format of DD/MM/YYYY. Year must be between 2000 and 2099.\n'
                )
