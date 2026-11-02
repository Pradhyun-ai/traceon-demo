"""Create labels, a milestone and demo issues in a GitHub repo.
Usage:  GITHUB_TOKEN=ghp_xxx python seed_github.py owner/repo
Windows PowerShell:  $env:GITHUB_TOKEN="ghp_xxx"; python seed_github.py owner/repo
No third-party packages needed."""
import json, os, sys, urllib.request, urllib.error

repo = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
token = os.environ.get("GITHUB_TOKEN") or sys.exit("Set GITHUB_TOKEN first")

def api(path, body):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        if e.code == 422:  # already exists
            return None
        sys.exit(f"GitHub said {e.code}: {e.read().decode()}")

LABELS = [("bug", "C2255C"), ("enhancement", "2F4BFF"), ("priority: high", "E03131"),
          ("priority: medium", "F08C00"), ("priority: low", "2F9E44"),
          ("status: to-do", "ADB5BD"), ("status: in-progress", "FAB005")]
for name, color in LABELS:
    api("/labels", {"name": name, "color": color})

ms = api("/milestones", {"title": "Sprint 1", "description": "Fix cart bugs, add receipts"})
if ms is None:
    sys.exit("Milestone 'Sprint 1' already exists. Use a fresh repo or delete it first.")

BUG = "**Steps to reproduce**\n{steps}\n\n**Expected**\n{exp}\n\n**Actual**\n{act}\n\nFile: `shop/cart.py`"
ISSUES = [
    ("Cart accepts negative quantities", ["bug", "priority: high", "status: to-do"],
     BUG.format(steps="`Cart().add('pen', 1.5, -2)`", exp="ValueError", act="Item added with qty -2, subtotal goes negative")),
    ("Removing a missing item crashes", ["bug", "priority: medium", "status: to-do"],
     BUG.format(steps="`Cart().remove('ghost')`", exp="Nothing happens", act="KeyError")),
    ("Discount total rounds to 1 decimal", ["bug", "priority: high"],
     BUG.format(steps="3 x 19.99, apply 15% discount", exp="50.97", act="51.0")),
    ("Average price crashes on empty cart", ["bug", "priority: low"],
     BUG.format(steps="`Cart().average_item_price()`", exp="0", act="ZeroDivisionError")),
    ("Add export_receipt() feature", ["enhancement", "priority: medium"],
     "As a shopper I want a text receipt listing items, quantities and total so I can keep a record.\n\nAcceptance: returns a string with one line per item and a total line."),
]
for title, labels, body in ISSUES:
    i = api("/issues", {"title": title, "body": body, "labels": labels, "milestone": ms["number"]})
    print("Created #%s %s" % (i["number"], title))
print("Done. Open Traceon and refresh.")
