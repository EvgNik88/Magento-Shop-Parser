import re
import time
import yaml

from playwright.sync_api import sync_playwright

URL = 'https://magento.softwaretestingboard.com/'


def is_valid_password(password):
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True


def create_registration_form(page, data):
    page.goto(URL, wait_until='domcontentloaded')
    page.click('//a[text()="Create an Account"]')

    page.fill('//*[@id="firstname"]', data['First Name'])
    page.fill('//*[@id="lastname"]', data['Last Name'])
    page.fill('//*[@id="email_address"]', data['Email'])
    page.type('//*[@id="password"]', data['Password'])
    time.sleep(5)
    page.fill('//*[@id="password-confirmation"]', data['Password'])

    if is_valid_password(data['Password']):
        page.get_by_title('Create an Account').click()
        assert page.url == 'https://magento.softwaretestingboard.com/customer/account/'

    else:
        assert page.locator('//*[@id="password-error"]').is_visible(), 'Error'


def test_main():
    with open('data.yaml', 'r') as file:
        data_list = list(yaml.safe_load_all(file))

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)

            for index, data in enumerate(data_list):
                context = browser.new_context()
                page = context.new_page()
                print(f'{index + 1} of {len(data_list)}')
                create_registration_form(page, data)

            browser.close()


if __name__ == "__main__":
    test_main()
