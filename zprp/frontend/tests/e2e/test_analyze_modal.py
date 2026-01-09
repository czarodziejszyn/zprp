from playwright.sync_api import expect


def test_analyze_modal_opens_and_populates(page, base_url: str):
    page.goto(base_url, wait_until="networkidle")
    page.click("#analyze-btn")
    modal = page.locator("#analysis-modal")
    expect(modal).to_be_visible()
    expect(page.locator("#modal-prices")).to_be_visible()
    expect(page.locator("#modal-chart")).to_be_visible()


def test_modal_close_with_backdrop(page, base_url: str):
    page.goto(base_url, wait_until="networkidle")
    page.click("#analyze-btn")
    expect(page.locator("#analysis-modal")).to_be_visible()
    page.click("#analysis-close")
    page.wait_for_timeout(200)
    style = page.locator("#analysis-modal").evaluate("el => getComputedStyle(el).display")
    assert style == "none"
