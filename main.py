import time
import csv
from playwright.sync_api import sync_playwright
import categories_for_parse as category


# URL = 'https://magento.softwaretestingboard.com/'
#
# CATEGORY_MEN = 'ui-id-5'
# CATEGORY_MEN_TOPS = 'ui-id-17'
# CATEGORY_MEN_HOODIES_AND_SWEATSHIRTS = 'ui-id-20'
# CATEGORY_MEN_BOTTOMS = 'ui-id-18'
# CATEGORY_MEN_PANTS = 'ui-id-23'


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
    page.locator('//*[@id="tab-label-additional"]').click()
    style_locator = page.locator('//td[contains(@data-th, "Style")]')
    product_information.append(style_locator.text_content() if style_locator.is_visible() else None)

    return product_information


def initialize_csv_writer():
    csvfile = open('Magento_Shop_Data.csv', 'w', newline='')
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


def process_category(page, csv_writer):
    category_locator = page.locator('//li[contains(@class, "item product")]').all()
    for index, item in enumerate(category_locator):
        item.click()
        page.wait_for_selector('//*[@class="swatch-option color"]')
        parsed_info = product_information_parser(page)
        csv_writer.writerow(parsed_info)
        print(f'{index + 1}/{len(category_locator)} is done...')
        page.go_back(wait_until='domcontentloaded')

    if has_next_page(page):
        next_page = page.locator('//a[@class="action  next"]').last
        next_page.click()
        page.wait_for_load_state('domcontentloaded')
        process_category(page, csv_writer)


def has_next_page(page):
    next_page = page.locator('//a[@class="action  next"]').last
    return next_page.is_visible()


def test_main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        csv_writer, csvfile = initialize_csv_writer()

        page.goto(category.URL, wait_until='domcontentloaded')

        goto_category(page, category.MEN, category.MEN_TOPS, category.MEN_HOODIES_AND_SWEATSHIRTS)
        process_category(page, csv_writer)

        goto_category(page, category.MEN, category.MEN_BOTTOMS, category.MEN_PANTS)
        process_category(page, csv_writer)

        csvfile.close()
        browser.close()


if __name__ == "__main__":
    test_main()
