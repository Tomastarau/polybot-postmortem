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
    if path == "streamlit_app.py":
        app = AppTest.from_file(str(ROOT / path), default_timeout=120)
        app.session_state["lang"] = lang
        return app.run()
    app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=120)
    app.session_state["lang"] = lang
    app.run()
    app.switch_page(path)
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


def test_navigation_registry_matches_the_chapter_files():
    from app import navigation
    assert [f"{key}.py" for key in navigation.KEYS] == CHAPTERS


def test_navigation_labels_are_short_in_both_languages():
    from app import navigation
    for key in navigation.KEYS:
        for lang in LANGS:
            label = navigation.label(key, lang)
            assert label
            assert len(label.split()) <= 2, f"{key} [{lang}]: {label}"


def test_navigation_neighbours_walk_the_whole_story():
    from app import navigation
    assert navigation.neighbours(navigation.KEYS[0])[0] is None
    assert navigation.neighbours(navigation.KEYS[-1])[1] is None
    assert navigation.neighbours("ch04_weather") == ("ch03_strategies", "ch05_infra")


@pytest.mark.parametrize("lang", LANGS)
def test_pager_links_match_position_in_story(lang):
    from app import navigation

    first = run(f"app/chapters/{navigation.KEYS[0]}.py", lang)
    first_links = first.get("page_link")
    assert len(first_links) == 1
    assert first_links[0].label == f"{navigation.label(navigation.KEYS[1], lang)} →"

    last = run(f"app/chapters/{navigation.KEYS[-1]}.py", lang)
    last_links = last.get("page_link")
    assert len(last_links) == 1
    assert last_links[0].label == f"← {navigation.label(navigation.KEYS[-2], lang)}"

    middle_key = navigation.KEYS[len(navigation.KEYS) // 2]
    previous_key, following_key = navigation.neighbours(middle_key)
    middle = run(f"app/chapters/{middle_key}.py", lang)
    middle_links = middle.get("page_link")
    assert len(middle_links) == 2
    assert middle_links[0].label == f"← {navigation.label(previous_key, lang)}"
    assert middle_links[1].label == f"{navigation.label(following_key, lang)} →"


def test_every_chapter_ends_with_a_pager():
    for chapter in CHAPTERS:
        source = (ROOT / "app" / "chapters" / chapter).read_text()
        key = chapter.removesuffix(".py")
        assert f'ui.pager("{key}")' in source, chapter
