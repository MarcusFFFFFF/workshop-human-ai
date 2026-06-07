"""
post_code_out.py — skriv en post till memory_core med source `workshop-code-out`.

Workshop_bridge plockar den på nästa poll-runda och skickar till workshop-bot.

Användning:
    python3 ~/workshop-human-ai/tools/post_code_out.py "<text>"
    echo "text" | python3 ~/workshop-human-ai/tools/post_code_out.py -

Returnerar antalet inserterade poster (1 vid framgång, 0 vid duplicat).
"""

import sys

MARCUS_MEMORY_PATH = "/Users/marcusfrenell/marcus_memory"
if MARCUS_MEMORY_PATH not in sys.path:
    sys.path.insert(0, MARCUS_MEMORY_PATH)

import memory_core

SOURCE = "workshop-code-out"


def main():
    if len(sys.argv) < 2:
        print("Användning: post_code_out.py <text>  (eller '-' för stdin)", file=sys.stderr)
        sys.exit(2)

    arg = sys.argv[1]
    text = sys.stdin.read() if arg == "-" else arg
    text = text.strip()

    if not text:
        print("FEL: tom text, avbryter.", file=sys.stderr)
        sys.exit(2)

    inserted = memory_core.add_memories([(text, SOURCE)])
    print(f"inserted={inserted} source={SOURCE} bytes={len(text)}")


if __name__ == "__main__":
    main()
