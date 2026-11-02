# Traceon demo experiment

A tiny shopping-cart library with 4 deliberate bugs and 1 missing feature.

## Setup
1. Create an empty GitHub repo (e.g. `traceon-demo`) and clone it.
2. Copy `shop/`, `tests/` and this README into it, then:
   git add . && git commit -m "Initial cart with known bugs" && git push
3. Seed the board:  GITHUB_TOKEN=ghp_xxx python seed_github.py YOURNAME/traceon-demo
4. `pip install pytest` and run `pytest`: 4 tests fail (that's the point).

## Demo script (about 5 minutes)
1. Traceon > Board: five issues in Sprint 1, sorted by status.
2. Open "Discount total rounds to 1 decimal" > **Create branch** (fix/3-discount-...).
3. `git fetch && git checkout fix/3-...`, change `round(..., 1)` to `round(..., 2)`, run `pytest` (one more test passes), commit, push.
4. Traceon > Branches > **Open pull request**, description: `Closes #3`.
5. Pull requests > **Squash and merge**. Issue #3 closes, the card moves to Done, Milestones shows progress rise.
6. Repeat for the other bugs; the feature can be a second sprint.
