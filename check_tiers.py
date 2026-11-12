"""Run the lab's official local checks for Easy, Medium, and Hard.

PyCharm: open this file and click Run. Reference stays local and gitignored.
Results: reports/tiers/SCORECARD.md and the per-task JSON files.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TASKS = ("easy_semantic", "medium_instance", "hard_panoptic")


def run(*arguments):
    print("\n>>>", " ".join(arguments), flush=True)
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main():
    output = ROOT / "reports" / "tiers"
    output.mkdir(parents=True, exist_ok=True)
    run("scripts/inspect_submissions.py", "--dir", "submissions")
    for task in TASKS:
        run("scoring/score.py", task, f"submissions/{task}.zip",
            "--group", "tiers", "--json", str(output / f"{task}.json"))
    run("scoring/scorecard.py", "--group", "tiers",
        "--dir", "submissions", "--out", "reports/tiers")
    print("\nOpen:", output / "SCORECARD.md", flush=True)
    print("Self-evaluation /82; checkpoints and official class grading are separate.", flush=True)


if __name__ == "__main__":
    main()
