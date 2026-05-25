from typing import Any
import core


def menu(data: dict[str, Any]) -> None:
    core.clear()

    print('\n-+ Options +-\n')
    core.print_menu(
        [
            'Colour mode',
            'Mark station as visited',
            'Reset visited stations',
            'Main menu',
        ]
    )

    while True:
        choice: str = input('> ')

        if choice == '1':
            change_clr_mode(data)
            break
        elif choice == '2':
            mark_visited(data)
            break
        elif choice == '3':
            reset_stations(data)
            break
        elif choice == '4':
            break
        else:
            print(
                '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
            )


def change_clr_mode(data: dict[str, Any]) -> None:
    core.clear()

    current_mode: str = 'Enhanced'

    if data['config']['use_enhanced_colours'] is False:
        current_mode = 'Native'

    print(
        'Configure how line colours are displayed by selecting one of the two modes. Accurate will use colours similar to the actual line colours; Native will use the colours defined by your terminal emulator.\n'
    )

    print(f'Current mode: {current_mode}\n')

    core.print_menu(['Use accurate colours', 'Use native colours', 'Main menu'])

    while True:
        choice: str = input('> ')
        if choice == '1':
            data['config']['use_enhanced_colours'] = True
            core.write(data)

            break
        elif choice == '2':
            data['config']['use_enhanced_colours'] = False
            core.write(data)

            break
        elif choice == '3':
            break
        else:
            print(
                '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
            )


def mark_visited(data: dict[str, Any]) -> None:
    core.clear()

    print(
        'To mark a station as visited, type in its name below. Type nothing to return to the main menu.\n'
    )

    station: str | None = core.fuzzy_search(data, True)

    if station:
        stn_data: dict[str, Any] = data['visited'].get(station) or data[
            'unvisited'
        ].get(station)

        visited: dict[str, Any] = data['visited'].get(station)

        if visited:
            print(
                f'\n{station} has already been marked as visited. Do you wish to set it back to being unvisited? (y/n)\n'
            )
            while True:
                user_input: str = input('> ')
                user_input = user_input.lower()

                if user_input == 'n':
                    input(
                        '\nOperation aborted. Press enter to return to the main menu.'
                    )
                    return

                elif user_input == 'y':
                    break

                else:
                    print(
                        '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
                    )

        if not visited:
            # Insert the dict associated with the user provided station into visited after grabbing it from unvisited with get(). Vice versa for the else statement.
            data['visited'].update({station: stn_data})

            # If the user provides a date, add on the date the station was visited to the station dict
            date: str | None = core.assign_date(station)

            if date:
                data['visited'][station].update({'date_visited': date})

            # Now that we've copied over the station dict into visited, we can remove it from unvisited with pop(). Vice versa for the else statement.
            data['unvisited'].pop(station)
        else:
            data['unvisited'].update({station: stn_data})
            # Remove the date_visited key from the station dict
            if data['unvisited'][station].get('date_visited'):
                data['unvisited'][station].pop('date_visited')

            data['visited'].pop(station)

        # If the station provided by the user was queued in to_visit, clear to_visit
        if data['to_visit'] == station:
            data['to_visit'] = ''

        # Write changes to datastore.json so the program remembers them when reopened
        core.write(data)

        input(
            '\nOperation completed successfully. Press enter to return to the main menu.'
        )


def reset_stations(data: dict[str, Any]) -> None:
    core.clear()

    core.console.print(
        'Warning! you are about to reset [bold underline]ALL VISITED STATIONS![/bold underline] Data that will be lost includes which stations have been visited and on what date you visited them. Type "I know what I\'m doing!" to reset all visited stations, or type anything else to return to the main menu.\n'
    )

    user_input: str = input('> ')

    if user_input == "I know what I'm doing!":
        visited = data['visited']
        # Get all keys (station names) in data['visited'] and turn it into a list so we know which stations we need to reset
        station_names: list[str] = list(visited.keys())

        # reset data['to_visit'] if it contains a value
        if len(data['to_visit']) > 0:
            data['to_visit'] = ''

        # Iterate over every key we got from data['visited'], remove any data that needs to be reset (like visited dates) then move the entire dict back to data['unvisited]
        for name in station_names:
            date_visited = visited[name].get('date_visited')

            if date_visited:
                visited[name].pop('date_visited')

            data['unvisited'].update({name: visited[name]})
            data['visited'].pop(name)

        core.write(data)

        input(
            '\nOperation succeeded - all visited stations have been reset. Press enter to return to the main menu.'
        )
    else:
        input('\nOperation cancelled. Press enter to return to the main menu.')
