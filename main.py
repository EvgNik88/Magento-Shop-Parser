import csv
from playwright.sync_api import sync_playwright

URL = 'https://magento.softwaretestingboard.com/geo-insulated-jogging-pant.html'


def test_run(page):
    page.goto(URL, wait_until='domcontentloaded')

    item_info = [
        page.locator('//*[@class="page-title"]').text_content().strip(),
        page.locator('//span[contains(@id,"product-price")]').first.text_content(),
        page.locator('//*[@class="product attribute description"]').text_content().strip(),
        page.locator('//td[contains(@data-th, "Material")]').text_content(),
        page.locator('//td[contains(@data-th, "Pattern")]').text_content(),
        page.locator('//td[contains(@data-th, "Climate")]').text_content()
    ]

    style_locator = page.locator('//td[contains(@data-th, "Style")]')
    if style_locator.is_visible():
        item_info.append(style_locator.text_content())
    else:
        item_info.append('-')

    with open('item_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Item Name', 'Item Price', 'Item Description', 'Material', 'Pattern', 'Climate', 'Style'])
        csv_writer.writerow(item_info)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    test_run(page)

    browser.close()
