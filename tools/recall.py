"""
recall.py — tunn wrapper för memory_core.search.

Användning:
    python3 ~/workshop-human-ai/tools/recall.py "<query>" [k] [min_score]

Exempel:
    python3 ~/workshop-human-ai/tools/recall.py "prompt caching"
    python3 ~/workshop-human-ai/tools/recall.py "F-15 survival frame" 10 0.4

Output: en blankradsseparerad lista över träffar med id, source, score, text.
"""

import sys

MARCUS_MEMORY_PATH = "/Users/marcusfrenell/marcus_memory"
if MARCUS_MEMORY_PATH not in sys.path:
    sys.path.insert(0, MARCUS_MEMORY_PATH)

import memory_core


def main():
    if len(sys.argv) < 2:
        print("Användning: recall.py <query> [k] [min_score]", file=sys.stderr)
        sys.exit(2)

    query = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
    min_score = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.35

    results = memory_core.search(query=query, k=k, min_score=min_score)

    if not results:
        print(f"(inga träffar för '{query}' över {min_score})")
        return

    for r in results:
        if not isinstance(r, dict):
            continue
        print(f"--- id={r.get('id')} src={r.get('source')} ts={r.get('ts')} score={r.get('score'):.2f}")
        print((r.get("text") or "").strip())
        print()


if __name__ == "__main__":
    main()
