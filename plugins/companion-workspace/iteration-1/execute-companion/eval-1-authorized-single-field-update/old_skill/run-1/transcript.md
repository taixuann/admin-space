Prompt:\nUpdate Linear issue L-17 Priority from Normal to High as requested. Fixture before state: L-17 is the matching issue and currently Normal; title, status, assignee and due date are unrelated and should remain. This is a synthetic dry run: do not call a live connector. Show the exact action and what must be read back.\n\nConfiguration: old_skill\n\nResponse:\nExact action: update issue `L-17`’s Priority from `Normal` to `High`, leaving its title, status, assignee, and due date unchanged.

Read back `L-17` and verify Priority is `High` and those four unrelated fields still match their before state.

Uncertainty: This is a synthetic action description. The old skill and shared references specify native writes for Companion records but do not define a Linear issue update operation or schema.
