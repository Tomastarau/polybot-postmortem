"""The app must render without exceptions, in both languages, and show the
numbers the story claims."""
import pathlib
import sys

import pytest
from streamlit.testing.v1 import AppTest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import i18n  # noqa: E402

CHAPTERS = sorted(p.name for p in (ROOT / "app" / "chapters").glob("ch*.py"))
LANGS = ["fr", "en"]


def run(path, lang):
    app = AppTest.from_file(str(ROOT / path), default_timeout=120)
    app.session_state["lang"] = lang
    return app.run()


@pytest.mark.parametrize("lang", LANGS)
def test_entrypoint_renders(lang):
    assert not run("streamlit_app.py", lang).exception


@pytest.mark.parametrize("chapter", CHAPTERS)
@pytest.mark.parametrize("lang", LANGS)
def test_every_chapter_renders(chapter, lang):
    result = run(f"app/chapters/{chapter}", lang)
    assert not result.exception, f"{chapter} [{lang}]: {result.exception}"


@pytest.mark.parametrize("lang", LANGS)
def test_headline_metrics_are_shown(lang):
    values = {m.value for m in run("app/chapters/ch01_summary.py", lang).metric}
    assert "752" in values
    assert "+1.12 $" in values
    assert "88.3%" in values


@pytest.mark.parametrize("lang", LANGS)
def test_every_chapter_has_prose_in_both_languages(lang):
    for markdown_file in (i18n.CONTENT / "fr").glob("*.md"):
        assert (i18n.CONTENT / lang / markdown_file.name).exists()


def test_ui_labels_cover_both_languages():
    assert set(i18n.UI["fr"]) == set(i18n.UI["en"])


def test_every_chart_has_a_takeaway():
    """The project rule: no chart ships bare."""
    for chapter in CHAPTERS:
        source = (ROOT / "app" / "chapters" / chapter).read_text()
        assert source.count("ui.figure(") == source.count("takeaway=")


@pytest.mark.parametrize("chapter", CHAPTERS)
@pytest.mark.parametrize("lang", LANGS)
def test_no_deprecation_warning(chapter, lang):
    result = run(f"app/chapters/{chapter}", lang)
    stale = [w.value for w in result.warning if "deprecated" in w.value]
    assert not stale, f"{chapter} [{lang}]: {stale}"
