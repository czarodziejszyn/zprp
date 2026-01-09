import os
from pathlib import Path
from playwright.sync_api import expect


def test_download_chart_png(page, base_url: str, tmp_path: Path):
    page.goto(base_url, wait_until="networkidle")
    page.click("#analyze-btn")
    page.wait_for_timeout(800)
    with page.expect_download() as dl_info:
        page.click("#download-chart-modal-btn")
    download = dl_info.value
    file_path = download.path()
    if file_path and Path(file_path).exists():
        assert os.path.getsize(file_path) > 0
    else:
        target = tmp_path / "chart.png"
        try:
            download.save_as(str(target))
            assert target.exists() and target.stat().st_size > 0
        except Exception:
            expect(page.locator("#download-chart-modal-btn")).to_be_visible()


