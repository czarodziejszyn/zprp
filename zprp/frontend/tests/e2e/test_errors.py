from playwright.sync_api import Route


def test_prices_error_message_when_blocked(page, base_url: str):
    def interceptor(route: Route):
        url = route.request.url
        if "/prices" in url:
            return route.fulfill(status=500, body=b"")
        return route.continue_()

    page.route("**/*", interceptor)
    page.goto(base_url, wait_until="networkidle")
    page.click("#analyze-btn")
    page.wait_for_timeout(2500)
    txt = page.locator("#modal-prices").inner_text() or ""
    assert "Błąd /prices: HTTP 500" in txt or "500" in txt
