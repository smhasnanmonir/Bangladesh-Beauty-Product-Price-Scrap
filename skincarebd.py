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
            url = f'https://skincarebd.com/shop/page/{page_number}/?v=fbd25224d617'
            print(f"Fetching page {page_number}: {url}")
            await page.goto(url)

            # Get all products on the page
            product_names = await page.query_selector_all('h5.mkd-product-list-title a')
            product_prices = await page.query_selector_all('span.price bdi')

            if not product_names:  # If no products are found, stop the loop
                print("No more products found, stopping.")
                flag = False
                break

            # Extract names and prices
            for name_element, price_element in zip(product_names, product_prices):
                product_name = await name_element.inner_text()
                product_price = await price_element.inner_text()
                product_price_slice = product_price[1:]
                products_list.append({"name": product_name, "price": product_price_slice})
                print(f"Product: {product_name}, Price: {product_price}")

            # Go to the next page
            page_number += 1

        # Save or print the final list of products
        print(json.dumps(products_list, indent=2))

        with open('Skincarebd.json', 'w') as json_file:
           json.dump(products_list, json_file, indent=2)

        print("Data saved to products_data.json")

        # Close the browser
        await browser.close()

def main():
    asyncio.run(run_playwright())

if __name__ == "__main__":
    main()
