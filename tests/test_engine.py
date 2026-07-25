"""Tests for identity resolution, the dedupe gate, and dossier merge."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import engine  # noqa: E402
import log  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    """Point every test at a throwaway ~/.outreach so real data is never touched."""
    monkeypatch.setenv("OUTREACH_HOME", str(tmp_path))
    return tmp_path


class TestResolveIdentity:
    def test_linkedin_url_wins(self):
        identity = engine.resolve_identity("https://www.linkedin.com/in/simonwillison/")
        assert identity.person_key == "simonwillison"
        assert identity.linkedin_url == "https://www.linkedin.com/in/simonwillison"

    def test_bare_x_handle(self):
        identity = engine.resolve_identity("@SimonW")
        assert identity.person_key == "simonw"
        assert identity.x_handle == "simonw"

    def test_x_url(self):
        identity = engine.resolve_identity("https://x.com/SimonW")
        assert identity.person_key == "simonw"

    def test_name_and_company(self):
        identity = engine.resolve_identity("Simon Willison, Datasette")
        assert identity.person_key == "simon-willison-datasette"
        assert identity.name == "Simon Willison"
        assert identity.company == "Datasette"

    def test_name_only(self):
        identity = engine.resolve_identity("Simon Willison")
        assert identity.person_key == "simon-willison"
        assert identity.company is None

    def test_accents_normalize(self):
        identity = engine.resolve_identity("Zoë Müller, Açme")
        assert identity.person_key == "zoe-muller-acme"

    def test_linkedin_beats_x_in_same_string(self):
        """Priority is fixed so one person always resolves to one key."""
        identity = engine.resolve_identity(
            "linkedin.com/in/simonwillison and x.com/simonw"
        )
        assert identity.person_key == "simonwillison"

    def test_empty_input_rejected(self):
        with pytest.raises(ValueError):
            engine.resolve_identity("   ")


class TestDedupeGate:
    def test_unknown_person_is_clean(self):
        result = engine.check_seen("nobody")
        assert result["contacted_before"] is False
        assert result["available_angles"] == list(log.ANGLES)
        assert result["exhausted"] is False

    def test_prior_contact_removes_its_angle(self):
        log.append_contact("simonw", "x", "shared-build", "hey", "https://example.com")
        result = engine.check_seen("simonw")
        assert result["contacted_before"] is True
        assert "shared-build" not in result["available_angles"]
        assert result["prior_contacts"][0]["message"] == "hey"

    def test_all_angles_used_marks_exhausted(self):
        for angle in log.ANGLES:
            log.append_contact("simonw", "x", angle, f"msg {angle}")
        result = engine.check_seen("simonw")
        assert result["exhausted"] is True
        assert result["available_angles"] == []

    def test_other_people_do_not_leak(self):
        log.append_contact("someone-else", "x", "shared-build", "hey")
        result = engine.check_seen("simonw")
        assert result["contacted_before"] is False


class TestDossier:
    def test_record_and_merge(self):
        engine.record_source("simonw", "x", {"bio": "builds things"})
        engine.record_source("simonw", "linkedin", "Staff Engineer at Acme")
        built = engine.build_dossier("simonw")

        assert built["usable"] is True
        assert set(built["sources_ok"]) == {"linkedin", "x"}
        assert built["sources_missing"] == ["web"]
        assert built["sources"]["x"]["bio"] == "builds things"

    def test_failed_source_is_visible_not_dropped(self):
        """A gap must stay visible so drafting never fills it silently."""
        engine.record_source("simonw", "x", None, status="failed")
        built = engine.build_dossier("simonw")

        assert built["sources_failed"] == ["x"]
        assert "x" not in built["sources"]
        assert built["usable"] is False

    def test_no_sources_is_unusable(self):
        engine.set_identity(engine.resolve_identity("@simonw"))
        assert engine.build_dossier("simonw")["usable"] is False

    def test_recording_twice_overwrites_not_duplicates(self):
        engine.record_source("simonw", "x", "old")
        engine.record_source("simonw", "x", "new")
        assert engine.build_dossier("simonw")["sources"]["x"] == "new"

    def test_unknown_source_rejected(self):
        with pytest.raises(ValueError):
            engine.record_source("simonw", "instagram", "hi")

    def test_identity_persists_into_dossier(self):
        engine.set_identity(engine.resolve_identity("Simon Willison, Datasette"))
        built = engine.build_dossier("simon-willison-datasette")
        assert built["identity"]["company"] == "Datasette"


class TestChooseChannel:
    def test_both_platforms_defers_to_nitesh(self):
        """The channel shapes the tone, so a real choice is never guessed."""
        engine.record_source("simonw", "linkedin", "Staff Engineer")
        engine.record_source("simonw", "x", {"bio": "builds things"})
        result = engine.choose_channel(engine.build_dossier("simonw"))

        assert result["ask"] is True
        assert result["channel"] is None
        assert set(result["options"]) == {"linkedin", "x"}

    def test_single_platform_resolves_without_asking(self):
        engine.record_source("simonw", "x", {"bio": "builds things"})
        result = engine.choose_channel(engine.build_dossier("simonw"))

        assert result["ask"] is False
        assert result["channel"] == "x"

    def test_override_wins_over_everything(self):
        engine.record_source("simonw", "linkedin", "Staff Engineer")
        engine.record_source("simonw", "x", {"bio": "builds things"})
        result = engine.choose_channel(engine.build_dossier("simonw"), override="linkedin")

        assert result["ask"] is False
        assert result["channel"] == "linkedin"

    def test_web_only_evidence_is_not_a_channel(self):
        """A personal site is a hook source, not somewhere you can DM."""
        engine.record_source("simonw", "web", ["https://simonwillison.net"])
        result = engine.choose_channel(engine.build_dossier("simonw"))

        assert result["channel"] is None
        assert result["ask"] is False
        assert result["options"] == []

    def test_failed_platform_is_not_an_option(self):
        engine.record_source("simonw", "linkedin", None, status="failed")
        engine.record_source("simonw", "x", {"bio": "builds things"})
        result = engine.choose_channel(engine.build_dossier("simonw"))

        assert result["channel"] == "x"
        assert result["options"] == ["x"]

    def test_bad_override_rejected(self):
        with pytest.raises(ValueError):
            engine.choose_channel(engine.build_dossier("simonw"), override="instagram")


class TestCli:
    def test_resolve_prints_json(self, capsys):
        engine.main(["resolve", "@simonw"])
        assert json.loads(capsys.readouterr().out)["person_key"] == "simonw"

    def test_seen_prints_json(self, capsys):
        engine.main(["seen", "simonw"])
        assert json.loads(capsys.readouterr().out)["exhausted"] is False
