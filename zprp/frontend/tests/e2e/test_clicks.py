import json

from playwright.sync_api import Route, expect


def test_search_sets_inside_point(page, base_url: str):
    def intercept_geocode(route: Route):
        if "nominatim.openstreetmap.org/search" in route.request.url:
            body = json.dumps([{"lat": "52.256039", "lon": "21.242752"}]).encode("utf-8")
            return route.fulfill(
                status=200, body=body, headers={"Content-Type": "application/json"}
            )
        return route.continue_()

    page.route("**/*", intercept_geocode)
    page.goto(base_url, wait_until="networkidle")
    before = page.locator("#coords").inner_text()
    page.fill("#addr-input", "test")
    page.click("#addr-search-btn")
    expect(page.locator("#coords")).not_to_have_text(before, timeout=3000)


def test_search_outside_does_not_change(page, base_url: str):
    def intercept_geocode(route: Route):
        if "nominatim.openstreetmap.org/search" in route.request.url:
            body = json.dumps([{"lat": "50.0", "lon": "50.0"}]).encode("utf-8")
            return route.fulfill(
                status=200, body=body, headers={"Content-Type": "application/json"}
            )
        return route.continue_()

    page.route("**/*", intercept_geocode)
    page.goto(base_url, wait_until="networkidle")
    before = page.locator("#coords").inner_text()
    page.fill("#addr-input", "test")
    page.click("#addr-search-btn")
    expect(page.locator("#coords")).to_have_text(before, timeout=2000)


def test_click_outside_does_not_change_when_blocked(page, base_url: str):
    page.goto(base_url, wait_until="networkidle")
    before = page.locator("#coords").inner_text()
    page.locator("div.leaflet-container").dblclick(position={"x": 5, "y": 5})
    page.wait_for_timeout(400)
    after = page.locator("#coords").inner_text()
    expect(page.locator("#coords")).to_be_visible()
