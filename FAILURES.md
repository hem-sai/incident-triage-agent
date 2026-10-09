# Failures Log

One line per real bug you hit while coding. Not "I was confused" — an actual bug: code that ran wrong, crashed, or gave the wrong answer, and what specifically fixed it.

Target: 10+ entries by Wk12, at least 3 with real before/after numbers (latency, complexity, cost), spread across 5+ different areas (DSA, Python, AWS, RAG, auth, deploy, etc.) — not all the same mistake repeated.

**Format (one line each):**
`YYYY-MM-DD · P0/P1/P2/P3 · area · what broke → what fixed it`

Severity key:
- P0 = broke everything (nothing runs / total blocker)
- P1 = major (a core feature is broken or badly wrong)
- P2 = annoying (works but cost you real time, or produced a wrong-but-not-obvious result)
- P3 = minor (typo-tier, caught fast, barely cost time)

---

## Entries

<!-- Add new entries below this line, newest at the bottom. New day: add a `---` line + `### 📅 YYYY-MM-DD` heading. Same day: separate entries with `- - -`. -->

### 📅 2026-09-25

2026-09-25 · P1 · DSA-hashing · `sorted(dict)` sorts keys only and drops the counts, so my Valid Anagram check (comparing sorted key lists) passed cases it shouldn't have (e.g. "xx" vs "x") → switched to `sorted(dict.items())` to sort key-value pairs, then simplified further since Python dict equality already ignores order — `d1 == d2` alone was sufficient. Source: dsa/2026-09-25-valid-anagram-a1.md

---

### 📅 2026-09-26

2026-09-26 · P2 · DSA-hashing · Top K Frequent: misread "k" as a frequency threshold instead of "return the k most frequent elements", so first attempt filtered by freq >= k and returned wrong elements entirely → researched sorting a dict by value (`sorted(d.items(), key=lambda x: x[1])`), then sliced `[:k]` to get exactly the k most frequent. Source: dsa/2026-09-26-top_k_frequent_elements-a1.md

- - -

2026-09-26 · P2 · Python-fileio · Exercises 6/7 in files_directories_path_exercises.ipynb called `.mkdir()` on paths meant to be files (`a.txt`, `main.py`, etc.), creating directories instead of files — went undetected because the PASS check only matched filenames via `rglob`, not file type → redone 9/27 using `.touch()` for both exercises, all checks now PASS. Note: the `.is_file()` assertion was not added to the check cells, so the underlying test gap (rglob matches by name/pattern only, not type) is still there — low risk now since creation is correct, but worth adding if this notebook gets reused. Source: python/files_directories_path_exercises.ipynb

---

### 📅 2026-09-27

2026-09-27 · P2 · Python-fileio · Cleanup cell (`shutil.rmtree(sandbox)`) threw `PermissionError: [WinError 5] Access is denied` on `exercise_sandbox/mixed/a.txt` — same Windows file-lock issue that showed up in files_directories_path.ipynb's cleanup on 9/26 (noted then, never actually fixed). Root cause not yet diagnosed (likely a stale handle or AV/indexer lock on a just-created file) → not fixed yet; needs either an `onexc` handler that retries after `os.chmod(path, stat.S_IWRITE)`, or a short retry loop around `rmtree`. Recurring across two notebooks now — fix it once, reuse the fix. Source: python/files_directories_path/files_directories_path_exercises.ipynb

---

### 📅 2026-09-29

2026-09-29 · P3 · DSA-arrays · Product of Array Except Self retry: typo'd `len(nums)` as `lens(nums)` in the prefix loop — would throw `NameError: name 'lens' is not defined` on run → caught and fixed to `len(nums)`. Didn't affect the actual logic gap (still needed help on the postfix multiply step), but caught fast, worth logging so it doesn't repeat. Source: dsa/2026-09-29-Products of Array Except Self_r1.md

---

### 📅 2026-09-30

2026-09-30 · P2 · Python-fundamentals · Set ops drill (Ex.8): called `set(a, b)` on two lists → `TypeError: set() takes at most 1 argument`, then tried `a | b` directly on the raw lists → same `TypeError` again (operator doesn't work on list), repeating the mistake without diagnosing it → had to Google set operators; fixed by converting both to `set()` first, then `&`, `-`, `|`. Real gap: forgot union/intersection/difference operators only work on `set` objects, not `list`. Source: python/method_drills/2026-09-30-method_drill.ipynb

- - -

2026-09-30 · P2 · Python-fundamentals · zip→dict drill (Ex.10): declared `rr = {}` as the target dict but the loop wrote `d[x] = y` instead — `d` was a leftover variable from Ex.4 (mississippi counter) still alive in the kernel, so the line ran with no error and silently wrote the scores into the wrong dict; `rr` stayed empty the whole time. Wrong-but-no-crash result from reusing a variable name across cells in the same session — would have gone undetected without a manual review. Source: python/method_drills/2026-09-30-method_drill.ipynb

- - -

2026-09-30 · P3 · Python-slicing · Slicing drill (Ex.5): used `nums[:-3]` for "last 3 elements" (actually returns everything *except* the last 3) and `nums[::3]` for "every 2nd element from index 1" (actually every 3rd from the start) — both backwards vs. what was asked, fixed in later cells as `nums[-3:]` and `nums[1::2]` but not logged per the drill's own "Attempt 2 (fix)" rule. Source: python/method_drills/2026-09-30-method_drill.ipynb

- - -

2026-09-30 · P3 · Python-stdlib · Counter drill (Ex.9): typo'd `Counter.` with nothing after the dot → `SyntaxError`, then had to Google to recall `Counter(s).most_common(2)`. Source: python/method_drills/2026-09-30-method_drill.ipynb

---

### 📅 2026-10-01

2026-10-01 · P2 · Python-fundamentals · Set-ops drill (Ex.1-iii): used `aa | bb` (union) when the exercise asked for symmetric difference → wrong answer, not caught during the drill itself (caught on review). Real gap: `|`=union, `^`=symmetric difference — these were conflated. Fix: use `aa ^ bb`. Source: python/method_drills/2026-10-01-method_drill.ipynb

- - -

2026-10-01 · P2 · Python-slicing · Last-4-elements drill (Ex.4): compared `nums[-1:-5:-1]` (reversed order) against `nums[len(nums)-4:]` (forward order) as if they should "confirm the same result" — they don't, element order differs, mismatch went uncaught. Fix: for matching order use `nums[-4:]`, not `nums[-1:-5:-1]`. Source: python/method_drills/2026-10-01-method_drill.ipynb

- - -

2026-10-01 · P2 · Python-stdlib/sorting · Counter+sort drill (Ex.8): task asked for "sorted by count descending, ties alphabetical" → code used `sorted(counted.items(), key=lambda item: item[1])` with no `reverse=True` and no tiebreak key — wrong order, no tiebreak, left unsolved with no second attempt. Source: python/method_drills/2026-10-01-method_drill.ipynb

- - -

2026-10-01 · P3 · Python-slicing · Stretch drill (Ex.6): first attempt sliced `nums[4:]` instead of `nums[5:]` for "last 5", and called `.extend()` without reversing first, then printed the `.extend()` call itself (returns `None`) instead of the result → fixed in a second cell (`nums[-1:-6:-1]` + correct `.extend()` + separate print), but the fix wasn't logged as a new documented attempt per the drill's own rule. Source: python/method_drills/2026-10-01-method_drill.ipynb

---

### 📅 2026-10-02

2026-10-02 · P2 · Python-stdlib/string-methods · Method-drill Ex.8(a): asked to split a path into "the first 2 pieces" using `maxsplit`, code used `path.split('/', maxsplit=2)` → produced 3 pieces (`['usr', 'local', 'share/configs/app.yaml']`), not 2. `maxsplit` counts the number of splits performed, not the number of resulting pieces (N splits → N+1 pieces) — classic off-by-one. Correctly used `maxsplit=1` on the very next line for part (b)'s `rsplit()`, so the concept wasn't totally missing, just applied inconsistently → fix: `path.split('/', maxsplit=1)` gives the actual 2 pieces (`['usr', 'local/share/configs/app.yaml']`). Source: python/method_drills/2026-10-02-method_drill.ipynb

- - -

2026-10-02 · P2 · Python-slicing · Method-drill Ex.2: this exercise exists specifically to re-drill 10/1's mistake (comparing a reversed slice to a forward slice as if they should match). Final check printed `nums[:-5:-1] == nums[6:]` directly → `False`, which only confirms the two slices don't match *as literally written*; the exercise's actual ask ("do they match once you account for the order difference?") needed one side reversed first, e.g. `nums[:-5:-1][::-1] == nums[6:]` → `True`. The reconciliation step from the hint was skipped, so the root gap from 10/1 (treating two differently-ordered slices as directly comparable) isn't fully closed — same issue, new wrapper. Source: python/method_drills/2026-10-02-method_drill.ipynb

- - -

2026-10-02 · P3 · Python-idioms · Method-drill Ex.6: grouping-into-lists exercise explicitly asked to build the list "on first use via `.get()`" — the idiom behind Group Anagrams / Top K-style problems (`groups[category] = groups.get(category, []); groups[category].append(word)`, or `.setdefault()`). Code instead used `.get()` only as an existence check inside `if groups.get(category, None) == None: ... else: ...`. Output was correct (`{'animal': ['cat', 'dog', 'eagle'], 'plant': ['rose', 'oak']}`) but the actual `.get()`-as-default-builder one-liner wasn't practiced, and `== None` was used instead of the idiomatic `is None`. Not a wrong answer — the targeted pattern for upcoming hashing-style DSA problems just didn't land yet. Source: python/method_drills/2026-10-02-method_drill.ipynb

- - -

2026-10-02 · P2 · DSA-complexity-analysis · Best Time to Buy/Sell Stock retry: code is a single pass tracking a running min price and max profit (`mi = min(mi, p); ma = max(ma, p - mi)` in one loop, no extra per-element storage) — that's O(n) time, O(1) space. Section 3 recorded it as O(n²) time / O(n) space, which doesn't match the algorithm actually written (and doesn't match the approach described in Section 2 either, which is a single iteration). Fix: when the code is one non-nested loop with no growing data structure, the complexity is O(n)/O(1) — go re-trace it line by line against what was written, not what the brute-force version "usually" is. Source: dsa/2026-10-02-Best Time to Buy-Sell Stock-r1.md

- - -

2026-10-02 · P2 · DSA-complexity-analysis · Majority Element first attempt: complexity recorded as O(n) time, but the code builds a count dict (O(n)) then calls `sorted(d.items(), key=..., reverse=True)` (O(k log k), k = distinct values, up to n) just to read off the single largest entry — real complexity is O(n log n) time, not O(n). This is the SECOND complexity miss today of the same shape (see the Best Time to Buy/Sell Stock entry above) — specifically, `sorted()`/`.sort()` calls aren't being counted into the stated Big-O. Fix either the analysis (say O(n log n) honestly) or the code (swap the sort for a single max-tracking pass, or `max(d, key=d.get)`, to actually hit O(n)). Source: dsa/2026-10-02-Majority Element-a1.md

---

### 📅 2026-10-03

2026-10-03 · P2 · Python-dict/sorting · Method-drill Ex.8: asked to sort a dict by value descending and print ONLY the top-2 KEYS (explicit example given: `["bob", "ann"]`, explicitly NOT `[("bob", 95), ("ann", 90)]`) — first attempt printed `sorted(scores.items(), key=..., reverse=True)[:2]` directly, i.e. the raw (key, value) tuples, the exact wrong shape the prompt had already ruled out. Attempt 2 tried `dict(aa).keys()` to recover, but that returns ALL 4 keys (no slicing applied after the dict conversion), still not top-2-only. Attempt 3 finally got it right: slice first (`aa[:2]`), then unpack just the key from each tuple (`[x for x, _ in aa[:2]]`) → `['bob', 'ann']`. Real gap: the sorting logic was correct from the first try every time — this was purely a result-shape/requirement-reading miss, same family as the 9/26 Top-K-Frequent "k" misread. Fix: when a prompt gives an explicit "not X, but Y" output example, check the printed value against that example before moving on, not just the sort order. Source: python/method_drills/2026-10-03-method_drill.ipynb

---

### 📅 2026-10-04

2026-10-04 · P2 · Python-dict/sorting · Method-drill Ex.10: prompt explicitly warned "print a list of just the name values... not the whole sorted list of dicts" (named as the same shape-discipline trap as Ex.1) — code computed `sorted_employees = sorted(employees, key=lambda emp: emp["salary"], reverse=True)` and printed that directly, never extracting `"name"` or slicing it down, the exact mistake the prompt pre-warned against. Third occurrence of this same shape-misread pattern (9/26 Top-K-Frequent "k" meaning, 10/3 Ex.8 top-2-keys-not-tuples) — not yet fixed. Fix: `[emp["name"] for emp in sorted_employees]`, and needs a clean redo in a future drill since the pattern is repeating, not a one-off. Source: python/method_drills/2026-10-04-method_drill.ipynb

---

### 📅 2026-10-07

2026-10-07 · P3 · DSA-two-pointers · Container With Most Water r1: first code moved both pointers every iteration (`L += 1; R -= 1`), skipping candidate pairs; self-caught and fixed to move only the shorter wall (`if height[L] < height[R]: L += 1 else: R -= 1`). Also stated Time as O(n^2) for what is a single-pass O(n) two-pointer solution, the same complexity-misstatement family as 10/2 and 10/6. Fix: before writing complexity, count passes over the input; a pointer pair that each move at most n steps is O(n). Source: dsa/Week-02_Oct-05_to_Oct-11/2026-10-07-Container With Most Water-r1.md

---

### 📅 2026-10-08

2026-10-08 · P3 · Python-string-methods · Method-drill Ex.9(b): prompt asked for keys joined by `", "` (comma + space), code used `",".join(sorted(kwargs))` → returned `level,name,team` instead of `level, name, team`. Sorting and `**kwargs` logic were right; just a delimiter misread. Fix: `", ".join(sorted(kwargs))`. Source: python/method_drills/2026-10-08-method_drill.ipynb

- - -

2026-10-08 · P2 · Python-dict/counting · Method-drill Ex.7: prompt (and the code comment) said characters appearing MORE than once, as a sorted list; first attempt used `d[c] > 2` and no `sorted()` → printed `['e']` instead of `['e', 'k', 'o']`, no crash, wrong answer went unnoticed until the morning review. Same misread-the-exact-ask habit as 10/8 Ex.9b (delimiter) and the result-shape misses on 10/3 and 10/4. Fix (Attempt 2 cell): `sorted([c for c in d if d[c] > 1])`. Habit fix: write the prompt phrase as a comparison in a comment ("more than once" = count > 1) before coding. Source: python/method_drills/2026-10-08-method_drill.ipynb
