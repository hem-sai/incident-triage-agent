from rag.evaluate import find_rank, hit_rate, mean_reciprocal_rank


def test_find_rank_is_one_based():
    assert find_rank(["RB-001", "RB-002", "RB-003"], "RB-001") == 1
    assert find_rank(["RB-001", "RB-002", "RB-003"], "RB-003") == 3


def test_find_rank_absent_is_zero():
    assert find_rank(["RB-001", "RB-002"], "RB-009") == 0
    assert find_rank([], "RB-001") == 0


def test_hit_rate_counts_only_ranks_within_k():
    ranks = [1, 0, 3, 2]
    assert hit_rate(ranks, 2) == 0.5
    assert hit_rate(ranks, 3) == 0.75


def test_mrr_treats_miss_as_zero():
    assert round(mean_reciprocal_rank([1, 0, 3, 2]), 3) == 0.458


def test_empty_ranks_do_not_divide_by_zero():
    assert hit_rate([], 3) == 0.0
    assert mean_reciprocal_rank([]) == 0.0
