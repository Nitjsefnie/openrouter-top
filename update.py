#!/usr/bin/env python3
"""Fetch OpenRouter's top 10 models by weekly tokens into top.json.

    update.py [--message FILE]

Rewrites top.json — just the model slugs in OpenRouter's weekly order — and
writes a commit message describing what moved since the previous file:
models that entered the top 10 (announced as new), models that left it, and
rank changes. Prints the message too.
"""
import argparse
import json
import os
import urllib.request

URL = "https://openrouter.ai/api/frontend/v1/models/find?order=top-weekly"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top.json")


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (openrouter-top)",
                                               "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        models = json.load(resp)["data"]["models"]
    return [{"slug": m["slug"]} for m in models[:10]]


def message(old, new):
    before = {m["slug"]: n for n, m in enumerate(old, 1)}
    after = {m["slug"]: n for n, m in enumerate(new, 1)}
    entered = [m for m in new if m["slug"] not in before]
    left = [m for m in old if m["slug"] not in after]
    moved = [m for m in new if m["slug"] in before and before[m["slug"]] != after[m["slug"]]]
    if entered:
        subject = f"Top 10: {len(entered)} new: " + ", ".join(m["slug"] for m in entered)
    elif moved:
        subject = f"Top 10: {len(moved)} rank change(s)"
    else:
        subject = "Top 10: order updated"
    body = [f"NEW  #{after[m['slug']]} {m['slug']}" for m in entered]
    body += [f"OUT  {m['slug']} (was #{before[m['slug']]})" for m in left]
    body += [f"MOVE {m['slug']} #{before[m['slug']]} -> #{after[m['slug']]}" for m in moved]
    return subject + ("\n\n" + "\n".join(body) if body else "") + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--message", help="write the commit message to this file")
    a = ap.parse_args()
    try:
        with open(DATA) as fh:
            old = json.load(fh)["models"]
    except FileNotFoundError:
        old = []
    new = fetch()
    if len(new) != 10:
        raise SystemExit(f"expected 10 models, got {len(new)}")
    msg = message(old, new)
    with open(DATA, "w") as fh:
        json.dump({"source": URL, "models": new}, fh, indent=2)
        fh.write("\n")
    if a.message:
        with open(a.message, "w") as fh:
            fh.write(msg)
    print(msg, end="")


if __name__ == "__main__":
    main()
