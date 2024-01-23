import time
import csv
from playwright.sync_api import sync_playwright

URL = 'https://magento.softwaretestingboard.com/'


def product_information_parser(page):
    product_information = [
        page.locator('//*[@class="page-title"]').first.text_content().strip(),
        page.locator('//span[contains(@id,"product-price")]').first.text_content(),
        page.locator('//*[@class="product attribute description"]').first.text_content().strip(),
        page.locator('//td[contains(@data-th, "Material")]').first.text_content(),
        page.locator('//td[contains(@data-th, "Pattern")]').first.text_content(),
        page.locator('//td[contains(@data-th, "Climate")]').first.text_content(),
        [color.get_attribute('aria-label') for color in page.locator('//*[@class="swatch-option color"]').all()]
    ]

    style_locator = page.locator('//td[contains(@data-th, "Style")]')
    product_information.append(style_locator.first.text_content() if style_locator.count() == 1 else None)

    return product_information


def initialize_csv_writer():
    csvfile = open('Magento_Shop_Parser.csv', 'w', newline='')
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ['Item Name', 'Item Price', 'Item Description', 'Material', 'Pattern', 'Climate', 'Colors', 'Style'])
    return csv_writer, csvfile


def goto_category(page, *category_ids):
    for category_id in category_ids:
        page.locator(f'//a[@id="{category_id}"]').hover()
        time.sleep(1)
    page.click(f'//a[@id="{category_ids[-1]}"]')
    page.wait_for_load_state('domcontentloaded')
    items = page.locator('//li[contains(@class, "item product")]').all()
    return items


def process_category(page, category_locator, csv_writer):
    for item in category_locator:
        item.click()
        page.wait_for_selector('//*[@class="swatch-option color"]')
        parsed_info = product_information_parser(page)
        csv_writer.writerow(parsed_info)
        page.go_back()


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        csv_writer, csvfile = initialize_csv_writer()

        page.goto(URL, wait_until='domcontentloaded')

        hoodies_and_sweatshirts = goto_category(page, 'ui-id-5', 'ui-id-17', 'ui-id-20')
        process_category(page, hoodies_and_sweatshirts, csv_writer)

        pants = goto_category(page, 'ui-id-5', 'ui-id-18', 'ui-id-23')
        process_category(page, pants, csv_writer)

        csvfile.close()
        browser.close()


if __name__ == "__main__":
    main()
