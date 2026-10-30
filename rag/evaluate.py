import json
import sys
from collections import defaultdict
from pathlib import Path

from rag.index import build_index
from rag.retrieve import ranked_runbook_ids

GOLDEN_PATH = Path(__file__).parent / "golden_set.json"


def find_rank(ranked_ids: list[str], expected_id: str) -> int:
    """1-based rank, 0 if absent."""
    for i, rid in enumerate(ranked_ids):
        if rid == expected_id:
            return i + 1
    return 0


def hit_rate(ranks: list[int], k: int) -> float:
    if not ranks:
        return 0.0
    hits = len([r for r in ranks if 1 <= r <= k])
    return hits / len(ranks)


def mean_reciprocal_rank(ranks: list[int]) -> float:
    if not ranks:
        return 0.0
    reciprocal = [1 / r if r != 0 else 0 for r in ranks]
    return sum(reciprocal) / len(reciprocal)


def summarize(ranks: list[int], ks: tuple[int, ...]) -> dict:
    row: dict = {"n": len(ranks)}
    for k in ks:
        row[f"hit@{k}"] = round(hit_rate(ranks, k), 3)
    row["mrr"] = round(mean_reciprocal_rank(ranks), 3)
    return row


def evaluate(store, ks=(3, 5)) -> dict:
    """Metrics overall and per question type, plus the questions that missed at min(ks)."""
    items = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    all_ranks: list[int] = []
    ranks_by_type: dict[str, list[int]] = defaultdict(list)
    misses = []

    for item in items:
        ranked = ranked_runbook_ids(store, item["question"])  # one search, read every k from it
        rank = find_rank(ranked, item["expected_runbook_id"])
        all_ranks.append(rank)
        ranks_by_type[item["type"]].append(rank)
        if not 1 <= rank <= min(ks):
            misses.append({
                "id": item["id"],
                "type": item["type"],
                "question": item["question"],
                "expected": item["expected_runbook_id"],
                "got": ranked[:min(ks)],
                "rank": rank,
            })

    result: dict = {"overall": summarize(all_ranks, ks)}
    for qtype, ranks in ranks_by_type.items():
        result[qtype] = summarize(ranks, ks)
    result["misses"] = misses
    return result


if __name__ == "__main__":
    # optional: python -m rag.evaluate 250 40
    size, overlap = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (500, 50)
    store = build_index(chunk_size=size, chunk_overlap=overlap)
    result = evaluate(store)
    misses = result.pop("misses")
    print(f"config chunk_size={size} overlap={overlap}")
    for name, row in result.items():
        print(f"{name:<11}", row)
    print(f"\nMissed at k=3: {len(misses)}")
    for m in misses:
        print(f"  {m['id']} [{m['type']}] {m['question']!r}")
        print(f"      expected {m['expected']} (rank {m['rank']}), got {m['got']}")
