# TODO

- [ ] **Usage logging follow-up (from Task 2).** `create_ticket` logs `input_tokens=0 output_tokens=0` because `with_structured_output(TriageResult)` returns only the parsed model, so the Bedrock usage numbers are lost. Options: `with_structured_output(TriageResult, include_raw=True)` and read `usage_metadata` from the raw message, or a LangChain usage callback. Then change the logging test (currently asserts 0) to the real numbers.
- [ ] Cache the runnable (`functools.lru_cache` on `get_runnable`) so a new `ChatBedrockConverse` is not built on every request. Keep it lazy so nothing calls AWS at import time.
- [ ] Add a test that `api.main` can be imported with no AWS credentials set.
- [ ] Decide what to do when the model's severity/category differs from the submitted ticket (real call on 10/24: ticket said `high`, model said `medium`).
