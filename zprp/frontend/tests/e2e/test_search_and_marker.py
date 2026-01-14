import re


def _coords_num(s: str):
    nums = re.findall(r"[-+]?\d+\.\d+", s or "")
    return tuple(map(float, nums)) if len(nums) >= 2 else None


def test_search_moves_marker(page, base_url: str):
    page.goto(base_url, wait_until="networkidle")
    before = page.locator("#coords").inner_text()
    addresses = [
        "Plac Defilad 1",
        "Marszałkowska 140",
        "Aleje Jerozolimskie 54",
        "Świętokrzyska 20",
        "Nowy Świat 15/17",
    ]
    changed = False
    for addr in addresses:
        page.fill("#addr-input", addr)
        page.click("#addr-search-btn")
        page.wait_for_timeout(2000)
        after = page.locator("#coords").inner_text()
        b = _coords_num(before)
        a = _coords_num(after)
        if b and a and a != b:
            changed = True
            break
    assert changed
