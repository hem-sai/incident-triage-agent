# RAG retrieval results

Golden set: 30 questions (20 paraphrase, 5 error_code, 5 confusable). Embedding: Titan v2. Retrieval fetches 50 chunks, deduplicated to runbook ids. Command: `python -m rag.evaluate <chunk_size> <overlap>`.

## Overall

| Config (size / overlap) | n | hit@3 | hit@5 | MRR |
|---|---|---|---|---|
| 250 / 40 | 30 |1 | 1| 0.978|
| 500 / 50 | 30 |1 |1 |0.983 |
| 1000 / 100 | 30 |0.967 | 1|0.958|

## By question type

### paraphrase (n=20)

| Config | hit@3 | hit@5 | MRR |
|---|---|---|---|
| 250 / 40 |1 |1 |1 |
| 500 / 50 |1 |1 | 1|
| 1000 / 100 |1 |1 |1 |

### error_code (n=5)

| Config | hit@3 | hit@5 | MRR |
|---|---|---|---|
| 250 / 40 |1 |1 | 1|
| 500 / 50 |1 | 1|1 |
| 1000 / 100 |1 |1 |1 |

### confusable (n=5)

| Config | hit@3 | hit@5 | MRR |
|---|---|---|---|
| 250 / 40 |1| 1| 0.867|
| 500 / 50 |1 |1 |0.9 |
| 1000 / 100 | 0.8| 1| 0.75|

## Noise caveat

With 30 questions, one question is 3.3 points, so differences under about 5 points are noise.

- The only hit@3 gap (1.0 vs 0.967) is one question, G-28, so it is inside the noise. hit@5 is 1.0 for all three configs.
- Paraphrase and error_code are 1.0 everywhere (ceiling effect), so this golden set cannot separate the configs on those types.
- The MRR spread (0.958 to 0.983) comes only from the 5 confusable questions, where n=5 makes each question worth 20 points. The 1000/100 weakness on confusable is a signal, not proof.

## Missed questions (rank 0 or > 3)

| Config | Question id | Type | Expected | Got (top 3) | Rank |
|---|---|---|---|---|---|
| 250 / 40 | none | | | | 0 misses |
| 500 / 50 | none | | | | 0 misses |
| 1000 / 100 | G-28 | confusable | RB-007 | RB-015, RB-029, RB-005 | 4 | 

## Choice

I choose 500/50: it has the best overall MRR (0.983), hit@3 and hit@5 of 1.0, and no misses, while 1000/100 dropped to hit@3 0.967 and confusable MRR 0.75 because one big chunk mixes several email topics. The trade-off is that 500/50 embeds 85 chunks against 30 for 1000/100 (131 for 250/40), and its confusable MRR (0.9) is still below 1.0; the gaps to 250/40 (0.978) are inside the noise, so this choice rests on cost and the confusable trend, not a clear win.
