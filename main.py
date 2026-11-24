#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800.

Writes one sentence (at most 200 characters) explaining the modern
internet to a time traveler who has just stepped out of the year 1800,
using only words and pictures a person from that year could already hold
in their head: libraries, post offices, letters, breakfast, tea, the sea.
The sentence must stand alone: no words coined after the traveler's time,
no list of features, just one picture — every library and post office on
earth folded into a single room, where a letter posted at breakfast is
read across the sea before your tea cools.

The program writes the sentence to /output/entry.txt and prints it to
stdout. The sentence is validated on every run and the program refuses
to write an invalid line.

Deterministic: no clock, no randomness, no network, stdlib only.
"""

import argparse
import os
import sys

SENTENCE = (
    "Imagine every library and post office on earth folded into one room, "
    "where a letter posted at breakfast is read across the sea before your "
    "tea cools."
)

OUTPUT_PATH = "/output/entry.txt"

MAX_SENTENCE_CHARS = 200


def validate_sentence(sentence: str) -> None:
    """Fail loudly unless the sentence is exactly one non-empty sentence.

    Exactly one sentence means: a single line, at most 200 characters,
    ending in one period, with no other sentence-ending punctuation
    anywhere in it.
    """
    if not sentence:
        raise ValueError("sentence must not be empty")
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("sentence must be exactly one line")
    if len(sentence) > MAX_SENTENCE_CHARS:
        raise ValueError(
            f"sentence is {len(sentence)} characters, over the "
            f"{MAX_SENTENCE_CHARS} limit"
        )
    if sentence.count(".") != 1 or not sentence.endswith("."):
        raise ValueError("sentence must end with exactly one period")
    if "?" in sentence or "!" in sentence:
        raise ValueError("sentence must not contain '?' or '!'")


def write_entry(path: str = OUTPUT_PATH) -> str:
    """Write the sentence to path (no trailing newline) and return it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(SENTENCE)
    return SENTENCE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Write one sentence explaining the modern internet to a "
        "traveler from 1800 to /output/entry.txt and print it. The sentence "
        "is validated first: exactly one sentence, non-empty, at most 200 "
        "characters.",
    )
    parser.add_argument(
        "--line",
        action="store_true",
        help="write and print the sentence (the default behaviour)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="only validate the sentence (one sentence, non-empty, at most "
        "200 characters) and exit 0 if it passes, 1 if it fails",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help="path of the entry file (default: /output/entry.txt)",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        validate_sentence(SENTENCE)
    except ValueError as exc:
        print(f"invalid sentence: {exc}", file=sys.stderr)
        return 1
    if args.verify:
        print(f"sentence valid: {len(SENTENCE)} characters, 1 sentence")
        return 0
    sentence = write_entry(args.output)
    print(sentence)
    return 0


if __name__ == "__main__":
    sys.exit(main())
