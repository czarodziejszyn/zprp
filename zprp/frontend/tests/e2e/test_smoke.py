from playwright.sync_api import expect


def test_home_loads(page, base_url: str):
    page.goto(base_url, wait_until="networkidle")
    expect(page.locator("div.leaflet-container")).to_be_visible()
    expect(page.locator("#coords")).to_be_visible()
    expect(page.locator("#analyze-btn")).to_be_visible()
