"""CHG-PW-006: draft site shell, DRAFT banner, privacy page, robots/noindex, fail-closed site check."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from pwatch.cli import main
from pwatch.site import (
    PRIVACY_EMAIL,
    ROBOTS_TXT,
    build_site,
    check_site,
    scan_html,
)

NOW = datetime(2026, 11, 19, 1, 30, tzinfo=timezone.utc)


@pytest.fixture
def built(tmp_path: Path) -> Path:
    out = tmp_path / "_site"
    build_site(out, commit="0" * 40, now=NOW)
    return out


def html_pages(out: Path) -> list[Path]:
    return sorted(out.rglob("*.html"))


def test_built_site_passes_check(built: Path) -> None:
    assert check_site(built) == []


def test_robots_txt_disallows_everything(built: Path) -> None:
    assert (built / "robots.txt").read_text(encoding="utf-8") == ROBOTS_TXT == "User-agent: *\nDisallow: /\n"
    assert not (built / "sitemap.xml").exists()


def test_every_page_has_noindex_draft_banner_csp_and_privacy_link(built: Path) -> None:
    pages = html_pages(built)
    assert {str(p.relative_to(built)) for p in pages} >= {"index.html", "privacy/index.html", "404.html"}
    for p in pages:
        html = p.read_text(encoding="utf-8")
        s = scan_html(html)
        assert s.robots == ["noindex, nofollow"], p
        assert s.draft_banner, p
        assert s.privacy_link, p
        assert s.csp and "default-src 'none'" in s.csp[0], p
        assert not s.has_script, p
        assert "<title>DRAFT · " in html, p


def test_privacy_page_role_contact_and_popia_wording(built: Path) -> None:
    html = (built / "privacy" / "index.html").read_text(encoding="utf-8")
    assert f'href="mailto:{PRIVACY_EMAIL}"' in html
    assert "public role only" in html
    for never in ("home addresses", "identity numbers", "personal phone numbers", "health information"):
        assert never in html
    assert "Right of reply: pending" in html
    assert "https://inforegulator.org.za/" in html
    assert "correction" in html
    assert "[legal wording unverified]" in html


def test_manifest_and_jekyll_config(built: Path) -> None:
    import json

    m = json.loads((built / "manifest.json").read_text(encoding="utf-8"))
    assert m["status"] == "draft" and m["build_id"] == "B20261119T013000Z"
    assert m["generated_at_sast"] == "2026-11-19T03:30:00+02:00"
    assert "index.html" in m["files"] and "robots.txt" in m["files"]
    assert "README.md" in (built / "_config.yml").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda h: h.replace('<meta name="robots" content="noindex, nofollow">', ""), "noindex"),
        (lambda h: h.replace("<strong>DRAFT.</strong>", "<strong>Note.</strong>"), "DRAFT banner"),
        (lambda h: h.replace("</main>", "<script>alert(1)</script></main>"), "<script>"),
        (lambda h: h.replace("</main>", "<p>someone@example.com</p></main>"), "e-mail address"),
        (lambda h: h.replace("</main>", "<p>Call 082 555 1234</p></main>"), "phone"),
        (lambda h: h.replace("</main>", "<p>8001015009087</p></main>"), "13-digit"),
        (lambda h: h.replace('href="/privacy/"', 'href="/x/"'), "/privacy/"),
        (lambda h: h.replace("</main>", '<img src="https://tracker.example/p.gif"></main>'), "external resource"),
    ],
)
def test_check_fails_closed_on_broken_page(built: Path, mutate, expected: str) -> None:
    p = built / "index.html"
    p.write_text(mutate(p.read_text(encoding="utf-8")), encoding="utf-8")
    fails = check_site(built)
    assert any(expected in f for f in fails), fails


def test_check_fails_on_changed_robots_or_sitemap(built: Path) -> None:
    (built / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (built / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
    fails = check_site(built)
    assert any("robots.txt" in f for f in fails) and any("sitemap" in f for f in fails)


def test_cli_build_and_check(tmp_path: Path) -> None:
    out = tmp_path / "s"
    assert main(["site", "build", "--out", str(out)]) == 0
    assert main(["site", "check", str(out)]) == 0
    (out / "privacy" / "index.html").unlink()
    assert main(["site", "check", str(out)]) == 2
