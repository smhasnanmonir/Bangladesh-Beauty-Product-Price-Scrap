import asyncio
import json
from playwright.async_api import async_playwright

async def run_playwright():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(20000)

        page_number = 1
        products_list = []
        flag = True

        while flag:
            url = f'https://beautybooth.com.bd/best-selling'
            print(f"Fetching page {page_number}: {url}")
            await page.goto(url)

            await page.wait_for_timeout(2000)

            # Get all products on the page
            product_names = await page.query_selector_all('h4.line-clamp-2')
            product_prices = await page.query_selector_all('p.font-bold')

            if not product_names:  # If no products are found, stop the loop
                print("No more products found, stopping.")
                flag = False
                break
            if page_number>20:
                break

            # Extract names and prices
            for name_element, price_element in zip(product_names, product_prices):
                product_name = await name_element.inner_text()
                product_price = await price_element.inner_text()
                product_price_slice = product_price[1:]
                products_list.append({"name": product_name, "price": product_price_slice})
                print(f"Product: {product_name}, Price: {product_price}")

            # Try to click the "Next" button to go to the next page
            try:
                next_button = await page.query_selector('button.w-9.sm\:w-fit.flex.items-center')
                if next_button:
                    page.click('button:nth-of-type(2)')
                    page_number += 1
                else:
                    flag = False  # No "Next" button means we're done
                    print("No Next button found, stopping.")
            except Exception as e:
                print(f"Error clicking the Next button: {e}")
                flag = False

        # Save the data to a JSON file
        with open('beautybooth.json', 'w') as json_file:
            json.dump(products_list, json_file, indent=2)

        print("Data saved to Skincarebd.json")

        # Close the browser
        await browser.close()

def main():
    asyncio.run(run_playwright())

if __name__ == "__main__":
    main()
