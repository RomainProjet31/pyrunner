import re

from src.game_properties_constants import Properties, GAME_PROPERTIES_FILE


# TODO: A lil sqlite database for da funz ?

def read_all_props() -> dict[str, any]:
    file = open(GAME_PROPERTIES_FILE, 'r')
    props: dict[str, any] = {}
    for line in file:
        if '=' in line:
            cur_str_prop = line.split('=')
            props[cur_str_prop[0]] = cur_str_prop[1]
    return props


def read(prop: Properties) -> any:
    props = read_all_props()
    if prop.value in props:
        match = re.match(r"^\d*", props[prop.value])
        return match.group(0) if match else None
    else:
        return None


def write(new_props: dict[Properties, any] = None) -> None:
    if new_props is not None:
        props = read_all_props()
        for key in new_props:
            props.update({key.value: new_props[key]})

        content = ""
        for key in props:
            content += f"{key}={props[key]}\n"

        file = open(GAME_PROPERTIES_FILE, 'w')
        file.write(content)
    else:
        print("Nothing to save")
