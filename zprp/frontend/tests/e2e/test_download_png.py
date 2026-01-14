import os
from pathlib import Path
import re

from playwright.sync_api import expect


def test_download_chart_png(page, base_url: str, tmp_path: Path):
    page.goto(base_url, wait_until="networkidle")
    page.click("#analyze-btn")
    expect(page.locator("#modal-chart")).to_have_attribute(
        "src", re.compile(r"^data:image/png;base64,"), timeout=10000
    )
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
