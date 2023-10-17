import logging
import os
import playwright.sync_api

BASE_URL = "https://game.maj-soul.com/1/"


def read_script(scripts_dir) -> str:
    with open(os.path.join(scripts_dir, "download.js"), "r") as f:
        return f.read()


def get_logs_on_page(logs_dir, scripts_dir, page, log_id):
    page.goto(f"{BASE_URL}?paipu={log_id}")
    page.wait_for_timeout(30 * 1000)
    js = read_script(scripts_dir)
    page.evaluate(js)
    logging.info("Downloading...")
    with page.expect_download() as download_info:
        page.keyboard.press("s")
    download = download_info.value
    logging.info(download.path())
    download.save_as(os.path.join(logs_dir, f"{log_id}.json"))
    page.wait_for_timeout(10 * 1000)


def download_all_logs(user_profile_dir: str, state_file: str, output_dir: str, scripts_dir: str, log_ids: list):
    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    with playwright.sync_api.sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_profile_dir, headless=False, channel="chrome")
        browser_context.storage_state(path=state_file)
        for log_id in log_ids:
            page = browser_context.new_page()
            try:
                get_logs_on_page(logs_dir, scripts_dir, page, log_id)
            except Exception as e:
                logging.error(e)
            finally:
                page.close()
