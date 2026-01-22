import json, argparse
from pathlib import Path

def count_key_values(data, target_key):
    types = {}

    for obj in data:
        if (target_key in obj):
            v = obj[target_key]
            if (v == 0):
                continue
            types[v] = types.get(v, 0) + 1

    return types

def rgb_to_hex(r, g, b, a = 255):
    r, g, b, a = int(r), int(g), int(b), int(a)
    hex_parts = [f"{x:02X}" for x in (r, g, b)]

    hex_color = '#' + ''.join(hex_parts)

    
    
    if (a != 255):
        hex_color += f"{a:02X}"
    else:
        match (hex_parts):
            case ['00', '00', '00']:
                hex_color = '#000'
            case ['FF', 'FF', 'FF']:
                hex_color = '#FFF'
    
    return hex_color

def convert(input) -> str:
    
    with open(input, 'r') as f:
        data = json.load(f)

    keys = count_key_values(data, "type")
    if (keys.get(5, 0) <= 0 or len(keys) > 1):
        print("You must only be using circles!")
        exit()

    del keys

    string = "<line-height=-.001>"

    for obj in data:
        if (obj['type'] == 0):
            continue

        dataY = obj['data'][1]
        dataScale = obj['data'][2]

        r = obj['color'][0]
        g = obj['color'][1]
        b = obj['color'][2]
        a = obj['color'][3]
        

        x = f'<space={obj['data'][0]}px>'
        y = f'<voffset={round((dataY - (dataScale * 1.9)) / 2)}px>'
        scale = f'<size={round(dataScale * 2.5)}>'
        color = f'<color={rgb_to_hex(r, g, b, a)}>'

        string += x + y + scale + color + "●<br>"
    
    return string

def batch(folder):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a valid directory")

    for fp in folder.glob("*.json"):
        output = fp.with_suffix(".txt")
        content = convert(fp)
        if content:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"converted! {fp.name} -> {output.name}")

def main():
    parser = argparse.ArgumentParser(description="Convert Geometrize data to TMP text objects")
    parser.add_argument("input", nargs='?', help="Path to input JSON file (ignored if --batch)")
    parser.add_argument("output", nargs='?', help="Path to output file (ignored if --batch)")
    parser.add_argument("--batch", help="Path to folder containing JSON files")

    args = parser.parse_args()

    if (args.batch):
        batch(args.batch)

    elif (args.input):
        content = convert(args.input)
        if (args.output):
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"converted! {args.input} -> {args.output}")
        else:
            print(content)

    else:
        parser.error("Must provide either --batch or input + output files")


if __name__ == "__main__":
    main()
    

    