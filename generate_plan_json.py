import subprocess
import re
import json
from pathlib import Path

# Path to your plan file
PLAN_FILE = Path("plan.txt")


def get_git_commits():
    # Get all commits touching plan.txt, oldest first
    result = subprocess.run(
        ["git", "log", "--reverse", "--format=%H|%ct", "--", str(PLAN_FILE)],
        stdout=subprocess.PIPE,
        text=True,
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        sha, ts = line.split("|")
        commits.append((sha, int(ts)))
    return commits


def get_file_at_commit(sha):
    # Dump the file content at a given commit
    result = subprocess.run(
        ["git", "show", f"{sha}:{PLAN_FILE}"],
        stdout=subprocess.PIPE,
        text=True,
        errors="ignore",
    )
    return result.stdout


def extract_entries(text):
    # Identify each entry starting with '+' and capture its content
    entries = []
    current = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("+"):
            # Commit previous entry
            if current:
                entries.append(current)
            # Start new entry, include text after '+'
            body_line = stripped[1:].strip()
            current = {"body": body_line + "\n"}
        elif current is not None:
            # Continuation lines
            current["body"] += line + "\n"
    # Append the last entry
    if current:
        entries.append(current)
    return entries


if __name__ == "__main__":
    commits = get_git_commits()
    seen = set()
    timeline = []

    for sha, ts in commits:
        content = get_file_at_commit(sha)
        for entry in extract_entries(content):
            body = entry["body"].strip()
            if body and body not in seen:
                seen.add(body)
                tags = re.findall(r"#(\w+)", body)
                timeline.append({
                    "timestamp": ts,
                    "commit": sha,
                    "body": body,
                    "tags": tags,
                })

    # Write out JSON
    out = Path("plan_log.json")
    out.write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    print(f"Generated {out} with {len(timeline)} entries")