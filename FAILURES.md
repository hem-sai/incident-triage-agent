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

### 📅 2026-10-06

2026-10-06 · P2 · DSA-two-pointers/complexity · Two Sum II first attempt: reused the plain Two Sum hash-map solution (`d[num] = index`, look up `target - num`) on a SORTED array. Output is correct, but it uses O(n) extra space and ignores the problem's O(1)-space constraint, which is the whole point of the sorted input (two pointers). Section 3 also recorded Time as O(n^2) when the single loop with O(1) dict lookups is O(n). Edge cases were written as "none". Two misses in one file: wrong tool for the constraint, and complexity stated without tracing the code. Fix: when the input is sorted, reach for two pointers (`L`, `R`, move `L` up if sum is too small, `R` down if too big) and state O(n) time / O(1) space; before writing Big-O, count passes over the input. Same under-stated-complexity family as 10/2 (twice) and 10/7. Source: dsa/Week-02_Oct-05_to_Oct-11/2026-10-06-two sum II-a1.md

---

### 📅 2026-10-07

2026-10-07 · P3 · DSA-two-pointers · Container With Most Water r1: first code moved both pointers every iteration (`L += 1; R -= 1`), skipping candidate pairs; self-caught and fixed to move only the shorter wall (`if height[L] < height[R]: L += 1 else: R -= 1`). Also stated Time as O(n^2) for what is a single-pass O(n) two-pointer solution, the same complexity-misstatement family as 10/2 and 10/6. Fix: before writing complexity, count passes over the input; a pointer pair that each move at most n steps is O(n). Source: dsa/Week-02_Oct-05_to_Oct-11/2026-10-07-Container With Most Water-r1.md

---

### 📅 2026-10-08

2026-10-08 · P3 · Python-string-methods · Method-drill Ex.9(b): prompt asked for keys joined by `", "` (comma + space), code used `",".join(sorted(kwargs))` → returned `level,name,team` instead of `level, name, team`. Sorting and `**kwargs` logic were right; just a delimiter misread. Fix: `", ".join(sorted(kwargs))`. Source: python/method_drills/2026-10-08-method_drill.ipynb

- - -

2026-10-08 · P2 · Python-dict/counting · Method-drill Ex.7: prompt (and the code comment) said characters appearing MORE than once, as a sorted list; first attempt used `d[c] > 2` and no `sorted()` → printed `['e']` instead of `['e', 'k', 'o']`, no crash, wrong answer went unnoticed until the morning review. Same misread-the-exact-ask habit as 10/8 Ex.9b (delimiter) and the result-shape misses on 10/3 and 10/4. Fix (Attempt 2 cell): `sorted([c for c in d if d[c] > 1])`. Habit fix: write the prompt phrase as a comparison in a comment ("more than once" = count > 1) before coding. Source: python/method_drills/2026-10-08-method_drill.ipynb

---

### 📅 2026-10-09

2026-10-09 · P3 · DSA-strings · Encode and Decode Strings r1 (length-prefix scheme): encode was right, decode had two bugs. (1) `length = int(s[index-1])` reads exactly one digit before `#`, so any word of length 10 or more decodes wrong (`"12#..."` gives 2, not 12). (2) A `for index, char in enumerate(s)` loop was nested inside `while i < len(s)`, so every pass rescanned the whole string from 0 and `i` was never used to resume where the last word ended; the first version also used `i <= len(s)` and `s[index-i]`. Needed help to land the fix. Fix: no `for`, walk with `i`: find the next `#` from `i` with a `j` pointer, `length = int(s[i:j])`, take `s[j+1 : j+1+length]`, then `i = j + 1 + length`. Edge cases listed ("numbers in string, separator") were never tested against the code. Source: dsa/Week-02_Oct-05_to_Oct-11/2026-10-09-encode decode string-r1.md

---

### 📅 2026-10-10

2026-10-10 · P2 · DSA-sets · Longest Consecutive Sequence a1: three bugs in one file. (1) `seen = set()` was never filled from `nums`, and the loop ran `for x in seen`, so it iterated an empty set and the function always returned 0. (2) The run-start check was inverted: `if x-1 in seen` instead of `if x-1 not in seen`, so it would have counted from the middle of runs, not the start. (3) `run` and `step` were mixed: `run` was incremented but never used, and `best = max(step, best)` compared the wrong variable. Approach, complexity and edge-case sections were left as the unfilled template, so none of this was caught before coding. Fix: `seen = set(nums)`, loop over `seen`, start a run only when `x-1 not in seen`, use one counter for the run length. See lessons/06-hash-set-sequence-starts.md. Source: dsa/Week-02_Oct-05_to_Oct-11/2026-10-10 longest consecutive sequence-a1.md

- - -

2026-10-10 · P2 · Python-fundamentals · Method-drill Ex.4 (chain walk): asked to keep moving "as long as the CURRENT key exists" in `next_step`; code used `while next_step[start] in next_step`, which checks the NEXT position, not the current one. On `a→b→c→d` it counted 2 steps instead of 3 (stopped one hop early), and it would raise `KeyError` if `start` were ever not a key. The printed final position (`d`) looked right only because it was read as `next_step[start]`. Off-by-one from checking the wrong end of the hop, uncaught during the drill. Fix: `while start in next_step: start = next_step[start]; count += 1`. Same chain-walk idea as the Longest Consecutive Sequence inner loop. Source: python/method_drills/2026-10-10-method_drill.ipynb

---

### 📅 2026-10-12

2026-10-12 · P2 · Python-fundamentals · Method-drill Ex.1 (chain walk, repeat of 10/10 Ex.4): wrote `while hop[start] in hop`, which checks the NEXT position, not the current one. On `a→b→c→d` it counted 2 steps instead of 3, and it would raise `KeyError` if `start` were not a key. The "on paper" count was also 2 (there are 3 arrows: a→b, b→c, c→d), so the miss started before the code. The printed final position (`d`) looked right only because it was read as `hop[start]`. Second time in 3 days for the same off-by-one. Fix: `while start in hop: start = hop[start]; count += 1`, then print `start`. Habit fix: test the loop on the first and the last node by hand before running. Source: python/method_drills/2026-10-12-method_drill.ipynb

- - -

2026-10-12 · P3 · Python-builtins · Method-drill Ex.3(a): asked whether EVERY cell is exactly one character; wrote `all(char for char in board_row if len(char)==1)==len(board_row)`, which filters inside the generator and compares a bool to a length, printing `False` when the answer is `True`. Fix: `all(len(cell) == 1 for cell in board_row)`. The condition goes in the expression, not in a trailing `if`. Source: python/method_drills/2026-10-12-method_drill.ipynb

- - -

2026-10-12 · P2 · Python-stdlib · Method-drill Ex.4: `defaultdict` took three attempts. Attempt 1 `defaultdict(col, set())` (TypeError: first argument must be callable), attempt 2 `defaultdict(set).append(dig)` (AttributeError: a set has `.add`, not `.append`, and the dict was re-created inside the loop), attempt 3 correct for (a). Then (b) `Counter(by_col)` counted the sets themselves, not the number of pairs per column; (c) and (d) not done before the stop. Fix: `by_col = defaultdict(set)` once, outside the loop, then `by_col[col].add(dig)`; for (b) `counts[col] += 1` with `defaultdict(int)`, or `Counter(col for col, _ in pairs)`. Source: python/method_drills/2026-10-12-method_drill.ipynb

- - -

2026-10-12 · P2 · DSA-hashing · Valid Sudoku a1: wrote `if digit in (rows[r], cols[c], boxes[box]): return False`. That asks "is the digit one of these three set objects?", so it compares a string to a tuple of sets and is never true. The function returned True for every board, including invalid ones, and no error was raised. Rows, columns and box index (`(r // 3) * 3 + c // 3`) were all right; the check itself was the bug. Fix: `if digit in rows[r] or digit in cols[c] or digit in boxes[box]: return False`, one `in` per set. Habit fix: before running, say out loud what `x in (a, b)` tests (equality against a and b, not membership inside them), and run one board that must return False. Got there by reading the lesson 05 walkthrough, so the file is "solved with help". Source: dsa/Week-03_Oct-12_to_Oct-18/2026-10-12-Valid sudoku-a1.md

---

### 📅 2026-10-13

2026-10-13 · P2 · DSA-hashing · Longest Consecutive Sequence a1: wrote the run-start check as `if x-1 in seen:` (backwards). That counts runs only from numbers that are NOT run starts, so every real start is skipped. The code returned `best - 1` for the test input and would return 0 when the list is one clean run. Fix: `if x-1 not in seen:`, so only the first number of a run starts the count. Habit fix: before running, say out loud what the `if` is selecting ("only numbers whose predecessor is missing"), then run `[100,4,200,1,3,2]` (expect 4). It was caught by running the sample, not by reading the code. The lesson 06 note already said `x - 1 not in seen`, so this was a transcription slip, not a missing concept. Source: dsa/Week-03_Oct-12_to_Oct-18/2026-10-13-longest consecutive sequence-a1.md

---

### 📅 2026-10-14

2026-10-14 · P1 · AWS-bedrock · `scripts/bedrock_hello.py` (`converse` on `amazon.nova-micro-v1:0`, eu-north-1) failed with `ValidationException: Operation not allowed`. Not a code or IAM bug: the IAM user has AdministratorAccess, and the same error came back for the `eu.` inference profile, Nova Lite, Nova 2 Lite, Claude Haiku 4.5 and us-east-1, so the block is account-wide. One probe in eu-west-1 returned `AccessDeniedException: Your account is currently being verified (normally < 2 hours)`, so the likely cause is a new AWS account still in verification / Bedrock not yet enabled for it. Side finding: in eu-north-1 the base ID `amazon.nova-micro-v1:0` only supports INFERENCE_PROFILE, so once the account is cleared use `eu.amazon.nova-micro-v1:0`. Second bug waiting behind it: `response["output"]["message"][0]["content"]` should be `response["output"]["message"]["content"][0]["text"]` (`message` is a dict, not a list). Fix: wait for verification and re-run, and if it persists after a few hours check Billing for a valid payment method and open an AWS Support case; then switch the model ID to the `eu.` profile and fix the response indexing. Habit fix: when an API error looks like a code bug, test a second model and region before changing code. Source: scripts/bedrock_hello.py

### 📅 2026-10-16

2026-10-16 · P3 · testing/deps · pytest warned that httpx is deprecated (TestClient dependency) -> installed httpx2, warning gone, CI #6 green

- - -

2026-10-16 · P1 · AWS-bedrock · Follow-up to the 14 Oct entry: the new Free-plan account stayed blocked for 3 days (14 to 16 Oct). `converse` returned `ValidationException: Operation not allowed` on every model and region, and AWS Support denied both cases ("can't approve your request... depends on regional factors, payment history, and account usage" and "account does not currently meet the eligibility requirements"). So this was an account-level eligibility block, not a code, IAM or quota problem. Fix: I switched the capstone credentials to my own main AWS account (IAM user, foundation models already available, no free credits). Checked in order: `sts.get_caller_identity` (right account), `bedrock.list_foundation_models` (123 models), `converse` on `amazon.nova-lite-v1:0` (worked), then `scripts/bedrock_hello.py` on `eu.amazon.nova-micro-v1:0` in eu-north-1 (worked). The first call on the main account returned `AccessDeniedException: Your account is currently being verified` once, then worked on retry; the cause is NOT established (an AI summary guessed backend propagation delay, which I could not verify). Before -> after: 0 successful Bedrock calls in 3 days -> working call, real cost from now on (cash cap $60, budget alerts to be set). Side finding: region mismatch, `Session().region_name` was `eu-north-1` while some tests ran in `us-east-1`; always pass `region_name` explicitly. Habit fix: when a vendor blocks the account, run the same code against a second account early instead of waiting on a support queue. Source: scripts/bedrock_hello.py


- - -

2026-10-16 · P2 · Python-logging · Task 3 request logging: first version set `status` with `"response" in locals()` checks in `finally`, which never matched, so every request would have logged `status=503`. After fixing that, I added `result, usage = triage_ticket(...)` inside the `try` and read `usage.get(...)` in `finally`, but `usage` was only assigned on success. On the 502 and 503 paths `triage_ticket` raised first, so `finally` raised `UnboundLocalError` and 6 tests failed (3 bad-model-output 502 cases, the 503 test, `test_logs_on_502`, `test_logs_on_503`). Before -> after: 6 failed / 8 passed -> 14 passed. Fix: set `status = "500"` and `usage: dict = {}` before the `try`, assign `status` in each branch, and read tokens with `.get(..., 0)`. Habit fix: a variable read in `finally` must be assigned before the `try`, because `finally` runs on every path, including the ones that fail early; the failure paths are the ones to test first. Source: api/main.py

---

### 📅 2026-10-18

2026-10-18 · P2 · testing/imports · Gate redo (blank file, `C:\gate_r1`): could not recall the TestClient import, so the clock stopped on a lookup before the first API test existed. Fix: `from fastapi.testclient import TestClient` (it lives under `fastapi.testclient`, not `fastapi`). Habit fix: write the three FastAPI test imports from memory once a day until they are automatic (`FastAPI`, `HTTPException`, `TestClient` is in the 18 Oct method drill). Source: tests/test_main.py

- - -

2026-10-18 · P2 · testing/pytest · Gate redo: the fixture that returns the TestClient was named `test_client`, but the tests asked for a parameter called `client`, so pytest could not match them. Fix: the fixture name must equal the argument name, so `@fixture def client(): return TestClient(app)` and `def test_valid(client, ...)`. Habit fix: write the test function signature first, then name the fixture to match it. Source: tests/test_main.py

- - -

2026-10-18 · P2 · testing/api · Gate redo: wrote `app.post("/incidents", json=...)` in the valid-body test instead of `client.post(...)`. `app` is the FastAPI object, where `.post` is the decorator that REGISTERS a route; `client` is the TestClient that SENDS a request. Fix: `res = client.post("/incidents", json=valid_ticket)`. Habit fix: in a test, the thing being called is always the client, never `app`. Source: tests/test_main.py

- - -

2026-10-18 · P2 · testing/pytest · Gate redo: forgot how to assert that bad data raises a validation error in the model test; could not recall `pytest.raises`. Fix: `with pytest.raises(ValidationError): Incident.model_validate(bad_data)` (the call that should fail goes INSIDE the `with`, and the test passes BECAUSE the error is raised). Habit fix: 18 Oct method drill Ex.5 and Ex.6 drill the import and the pattern. Source: tests/test_model.py

- - -

2026-10-18 · P3 · lint/ruff · Found by the coach reading `C:\gate_r1`: `res = Incident.model_validate(invalid)` inside the `pytest.raises` block assigns a variable that is never used, so `ruff check .` reports F841 and the capstone CI ruff step would go red on the same pattern. Fix: drop the assignment and call `Incident.model_validate(invalid)` on its own. Habit fix: run `ruff check .` before saying a drill is done. Source: tests/test_model.py

---

### 📅 2026-10-19

2026-10-19 · P2 · api/dependency-injection · `api/main.py` read-aloud (missed question 1 from 17 Oct): could not say why `create_ticket` takes `client=Depends(get_bedrock_client)` instead of creating the boto3 client inside the function or at module level. Reason: `Depends` makes FastAPI call `get_bedrock_client()` for each request and pass the result in as `client`. The route never builds its own client, so (1) tests can swap it with `app.dependency_overrides[get_bedrock_client] = lambda: fake_client` and run with zero AWS calls, which is how the 502 and 503 tests work; (2) the region and the timeout/retry `config` live in one place; (3) nothing talks to AWS or needs credentials at import time. Fix: say it as "the dependency is the seam where tests replace Bedrock". Side note: as written, a new boto3 client is built on every request; fine for now, cache it if latency matters later. Habit fix: before saying a line of `main.py` is understood, name what breaks if it is removed (here: tests would need real AWS). Source: api/main.py

- - -

2026-10-19 · P2 · api/timeouts · `api/main.py` read-aloud (missed question 2 from 17 Oct): did not understand `Config(connect_timeout=15, read_timeout=30, retries={"max_attempts": 3, "mode": "standard"})`. Now understood. `connect_timeout` is the longest wait (seconds) to open the network connection to the Bedrock endpoint; if it is hit, the call fails before any model work starts, so it points at network or endpoint trouble. `read_timeout` is the longest wait for the response bytes after the request was sent; with `converse` (not streaming) the model's whole generation time counts as waiting, so a slow or long answer over 30 s fails even though Bedrock is still working. Retries in `standard` mode re-send on timeouts, so per botocore docs one request can take several times 30 s before it finally fails (worst case roughly 2 min with 1 try + 3 retries), which is longer than most API gateways and clients will wait. Fix: pick the timeouts from the real latency numbers (Wk12), and keep the worst case (timeout x attempts) under the caller's own limit. Habit fix: when a config value has a number, write the unit and the worst case next to it in the code comment. Source: api/main.py

---

### 📅 2026-10-21

2026-10-21 · P2 · api · botocore timeouts returned 500 instead of 503: `ReadTimeoutError` and `ConnectTimeoutError` derive from `BotoCoreError`, not `ClientError`, so `except ClientError` in `create_ticket` missed them and the exception escaped as an unhandled 500 ("your code is broken" instead of "try again later"). Proved first with `test_timeout_returns_503` (fake client raising `ReadTimeoutError(endpoint_url="https://bedrock")`): it failed with the raw `ReadTimeoutError`. Before -> after: 1 failed -> passing. Fix: `except (ClientError, BotoCoreError)` in api/main.py, so both timeout classes (and other botocore client-side errors) map to 503. Habit fix: before relying on an `except`, check the exception's base classes (`ReadTimeoutError.__mro__`) and write the failing test first. Source: api/main.py, tests/test_api.py

---

### 📅 2026-10-23

2026-10-23 · P2 · DSA-sliding-window · you removed s[right] from the set instead of s[left] → corrected to window_state.remove(s[left])

---

### 📅 2026-10-24

2026-10-24 · P1 · api/dependency-injection · Task 2 (structured output): rewrote `triage_ticket` to call `runnable.invoke(prompt)` but left `get_bedrock_client()` in `api/main.py` as the dependency, so the route would have passed a raw boto3 client into `.invoke()`. A boto3 client has no `.invoke`, so every request would raise `AttributeError`, which no `except` catches, so every ticket would return 500. Found on review before the first real call, not by a test. Fix: `def get_runnable(): return build_triage_runnable()` and `Depends(get_runnable)`. The model is still built lazily, so nothing calls AWS at import time. Habit fix: when a function's parameter changes type (client to runnable), grep for every caller and every `Depends` that feeds it before running. Source: api/main.py

- - -

2026-10-24 · P2 · api/timeouts · Task 2: the botocore `Config(connect_timeout=15, read_timeout=30, retries=...)` stayed in `api/main.py` and only fed the old boto3 client. `ChatBedrockConverse(...)` was built without it, so the LangChain call silently ran on default timeouts and retries, and the 503 timeout mapping from 10/21 would have been guarding settings that no longer applied. Nothing crashed, so no test noticed. Fix: move `config` into `api/triage.py` and pass `config=config` to `ChatBedrockConverse`; delete the dead `get_bedrock_client`, `boto3` and `Config` from main.py. Habit fix: after swapping a client, list every setting the old one carried (region, timeouts, retries) and check each one reached the new one. Source: api/triage.py, api/main.py

- - -

2026-10-24 · P2 · testing/dependency-overrides · Task 3: tests were half-migrated. `make_client` first still overrode `get_bedrock_client`, which nothing depends on anymore, so the override did nothing and every test would have called the real `get_runnable()` and hit AWS. Then `FakeRunnable` had no `invoke`, tests still passed `text=` to it, the old `FakeClient.converse` fakes no longer matched, and `TimeoutClient` / `FailingRunnable` were deleted but still used (ruff F821 on both). Before -> after: 13 ruff errors and a suite that would call AWS -> ruff clean and 19 passed, zero AWS calls. Fix: one `FakeRunnable(result=None, error=None)` with `.invoke(prompt)`, override `get_runnable`, and rewrite the old tests (bad-JSON cases deleted, since the output is no longer parsed by my code; token log assertions changed to 0). Habit fix: after changing a dependency, check that the test override key is the same function the route uses, and run the suite with no AWS credentials to prove nothing escapes. Source: tests/test_api.py

- - -

2026-10-24 · P3 · lint/ruff · Task 4: `uv run ruff check .` reported 13 errors: the old `_triage_ticket` and `import json` left in `api/triage.py`, an unused `MODEL` constant, an inner import inside `get_runnable()`, unsorted imports, about 10 unused imports in tests/test_api.py, and two E712/E501 hits in the untracked `scratch/` scripts. Fix: delete the dead code, `ruff check . --fix`, and add `exclude = ["scratch"]` to `[tool.ruff]`. Also removed the leftover "Reply should contain only the keys..." prompt line, since `with_structured_output` already carries the schema. Habit fix: run `ruff check .` after every refactor, not only at the end. Source: api/triage.py, tests/test_api.py

- - -

2026-10-24 · P3 · shell/windows · Task 4.1: pasted `curl -X POST ... -d @ticket.json` into PowerShell. There `curl` is an alias for `Invoke-WebRequest`, which has no `-X` / `-H` in curl's meaning, and `@ticket.json` is parsed as splatting (`SplattingNotPermitted`, then `Cannot bind parameter 'Headers'`). The request never reached the API. Fix: `curl.exe` (the real binary) with the path quoted: `curl.exe -X POST localhost:8000/tickets -H "Content-Type: application/json" -d "@ticket.json"`. Habit fix: on Windows PowerShell always type `curl.exe`. Source: ticket.json

- - -

2026-10-24 · P3 · tooling/files · Task 4.1: after switching to `curl.exe`, it failed with `Failed to open ticket.json` because the task said to use a JSON file but I never created one. Fix: create `ticket.json` (a body matching the `Ticket` model) in the folder curl runs from; the real call then returned 200 `{"category":"network","severity":"medium","confidence":0.85}`. Habit fix: when a step says "use file X", `ls` for it first. Source: ticket.json

- - -

2026-10-24 · P2 · ci/dependencies · Pushed Task 2-4 and CI went red: `pytest` failed at collection with `ModuleNotFoundError: No module named 'langchain_aws'` (traceback: tests/test_api.py → api/main.py → api/triage.py:4). The workflow installs its own hand-typed list (`pip install "fastapi[standard]" boto3 httpx2 pydantic pytest ruff`) instead of reading `pyproject.toml`, so the new `langchain-aws` dependency was never installed there. It passed locally because `uv run` installs from `pyproject.toml` / `uv.lock`; `ruff check .` passed in CI because ruff does not import code. Before -> after: 1 collection error (6 of 19 tests collected, `test_api.py` never loaded) -> fix pushed. Fix: add `"langchain-aws>=1.9.0"` to the `pip install` line in `.github/workflows/ci.yml`; switching CI to `uv sync` + `uv run pytest` so it uses the lockfile is a separate decision. Habit fix: when a commit adds an import of a new package, add it to the CI install step in the same commit, and check the workflow's install line against `pyproject.toml`. Source: .github/workflows/ci.yml
