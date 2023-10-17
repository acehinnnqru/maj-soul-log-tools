import playwright.sync_api


def __save_state(browser: 'playwright.sync_api.Browser', fp: str, url, timeout: int = 60 * 1000):
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(timeout)

    page.context.storage_state(path=fp)


# this may require you to manually login in 60 seconds
def manual_save_state(fp: str, url: str, timeout: int = 60 * 1000):
    with playwright.sync_api.sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        __save_state(browser, fp, url, timeout=timeout)
        browser.close()
