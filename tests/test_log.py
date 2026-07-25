"""Tests for the append-only outreach record."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import log  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTREACH_HOME", str(tmp_path))
    return tmp_path


def test_append_creates_file_and_parent_dir(isolated_home):
    log.append_contact("simonw", "x", "shared-build", "hey")
    assert (isolated_home / "sent.jsonl").exists()


def test_append_is_append_only():
    log.append_contact("simonw", "x", "shared-build", "first")
    log.append_contact("simonw", "linkedin", "direct-ask", "second")
    rows = log.contacts_for("simonw")
    assert [row["message"] for row in rows] == ["first", "second"]


def test_bad_angle_rejected_at_write():
    """Typos must fail loudly, or dedupe would never match the row later."""
    with pytest.raises(ValueError):
        log.append_contact("simonw", "x", "direct_ask", "hey")


def test_bad_channel_rejected():
    with pytest.raises(ValueError):
        log.append_contact("simonw", "instagram", "direct-ask", "hey")


def test_corrupt_line_does_not_hide_history(isolated_home):
    log.append_contact("simonw", "x", "shared-build", "good")
    with (isolated_home / "sent.jsonl").open("a", encoding="utf-8") as handle:
        handle.write("{not json\n")
    log.append_contact("simonw", "x", "direct-ask", "also good")

    assert len(log.contacts_for("simonw")) == 2


def test_missing_file_returns_empty():
    assert log.contacts_for("nobody") == []
    assert log.available_angles("nobody") == list(log.ANGLES)


def test_angles_are_scoped_per_intent():
    """Networking in March must not block a role ask in July."""
    log.append_contact("simonw", "x", "shared-build", "hey", intent="network")

    assert "shared-build" not in log.available_angles("simonw", "network")
    assert "shared-build" in log.available_angles("simonw", "job")


def test_exhausting_one_intent_leaves_others_open():
    for angle in log.ANGLES:
        log.append_contact("simonw", "x", angle, f"m {angle}", intent="network")

    assert log.available_angles("simonw", "network") == []
    assert log.available_angles("simonw", "job") == list(log.ANGLES)


def test_unscoped_query_counts_every_intent():
    log.append_contact("simonw", "x", "shared-build", "a", intent="network")
    log.append_contact("simonw", "x", "direct-ask", "b", intent="job")

    assert log.used_angles("simonw") == {"shared-build", "direct-ask"}


def test_legacy_row_without_intent_blocks_every_intent(isolated_home):
    """An unlabeled past message might have used this angle. Assume it did."""
    import json
    path = isolated_home / "sent.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "person_key": "simonw", "channel": "x", "angle": "direct-ask",
        "date": "2026-01-01T00:00:00+00:00", "message": "old",
    }) + "\n", encoding="utf-8")

    assert "direct-ask" not in log.available_angles("simonw", "job")
    assert "direct-ask" not in log.available_angles("simonw", "network")


def test_bad_intent_rejected():
    with pytest.raises(ValueError):
        log.append_contact("simonw", "x", "direct-ask", "hey", intent="friendship")


def test_intent_defaults_to_job():
    row = log.append_contact("simonw", "x", "direct-ask", "hey")
    assert row["intent"] == "job"


def test_used_and_available_are_complementary():
    log.append_contact("simonw", "x", "recent-thing", "hey")
    assert log.used_angles("simonw") == {"recent-thing"}
    assert "recent-thing" not in log.available_angles("simonw")
