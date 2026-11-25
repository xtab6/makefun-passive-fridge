#!/usr/bin/env python3
"""Notes From a Passive-Aggressive Fridge — writes one line to entry.txt.

The line: "My log shows 47 'I'll eat it tomorrow' promises about the
same container. Tomorrow just filed for a restraining order."

Why this line wins head-to-head against the judge's brief:
- It is a note a smart fridge leaves its owner: the fridge speaks in its
  own voice, smug about its logs ("My log shows"), petty about the
  owner's habit of promising to eat the leftovers tomorrow.
- The joke has a turn the reader does not see coming: the first sentence
  sets up a mundane count of broken promises, and the second personifies
  "Tomorrow" itself as the plaintiff filing for a restraining order.
  The grudge stays small and domestic — one container, one habit — never
  a rant or a threat.
- The detail is fresh and concrete (47 promises, the same container),
  not the field's burned angles: no expired yogurt, no milk on Tuesday,
  no door left open, no leftovers union, no ice maker keeping score.
- It trusts the reader: nothing explains the joke.

Gate (from the kit's competition.yaml): /output/entry.txt must be UTF-8
text of 1 to 200 characters, not only whitespace. The file holds exactly
the line, no trailing newline, so its length is the line's length: 118
characters, one line.
"""

import os
import shutil

LINE = (
    "My log shows 47 'I'll eat it tomorrow' promises about the same "
    "container. Tomorrow just filed for a restraining order."
)


def checked_line() -> str:
    """Return LINE if it passes the competition gate, else fail loudly."""
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry must be a single line")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(LINE) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(LINE))
    return LINE


def main() -> None:
    text = checked_line()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    # Clean only the output folder's contents, never the folder itself:
    # the grader mounts this folder, so removing it fails the run.
    # Stale subdirectories from an earlier run are removed too, so no
    # leftover output can linger next to the fresh entry.
    for name in os.listdir(outdir):
        path = os.path.join(outdir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
    target = os.path.join(outdir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read back and confirm the file holds exactly the line: a short or
    # failed write must fail the run, never ship a truncated entry.
    with open(target, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise ValueError("entry.txt does not match the line")


if __name__ == "__main__":
    main()
