import asyncio
import json
from playwright.async_api import async_playwright

async def run_playwright():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        page_number = 1
        products_list = []
        flag = True

        while page_number == 1:
            # Navigate to the target URL (for the first page)
            url = f'https://cityshop.com.bd/hair-care'
            await page.goto(url)

            # Wait for 7 seconds to ensure the page loads completely
            await asyncio.sleep(7)

            # Optionally, ensure specific elements are loaded
            await page.wait_for_selector("a.product_name_link h2")
            
            # Get all product names and prices
            product_name_elements = page.locator("a.product_name_link h2")
            product_price_elements = page.locator("span.product_new_price")

            # Count the number of products found
            product_count = await product_name_elements.count()

            if product_count == 0:  # If no products are found, stop the loop
                print("No more products found, stopping.")
                flag = False
                break

            for i in range(product_count):
                product_name = await product_name_elements.nth(i).text_content()
                product_price = await product_price_elements.nth(i).text_content()
                product_price_clean = product_price.strip()  # Clean whitespace if needed
                products_list.append({"name": product_name, "price": product_price_clean})
                print(f"Product: {product_name}, Price: {product_price_clean}")

            # Move to the next page
            page_number += 1

        # Save the final list of products to a JSON file
        with open('cityShop_hair.json', 'w') as json_file:
            json.dump(products_list, json_file, indent=2)

        print("Data saved to cityShop.json")

        # Close the browser
        await browser.close()

def main():
    asyncio.run(run_playwright())

if __name__ == "__main__":
    main()
