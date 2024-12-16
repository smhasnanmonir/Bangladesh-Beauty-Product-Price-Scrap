import asyncio
import json
from playwright.async_api import async_playwright

async def run_playwright():
    async with async_playwright() as p:
        # Launch Firefox browser (headless=False for debugging)
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        # Go to the page
        await page.goto('https://koreanmartbd.com/product-category/skin-care/')
        await asyncio.sleep(3)

        products_list = []
        seen_products = set()  # To avoid redundancy
        scroll_count = 250  # Set the number of times to scroll

        # Wait for the product container to load
        try:
            await page.wait_for_selector("h3.wd-entities-title a")
        except Exception as e:
            print(f"Error waiting for product container: {e}")
            return

        # Scroll 35 times
        for i in range(scroll_count):
            # Get the viewport height (height of the visible part of the browser window)
            viewport_height = await page.evaluate("window.innerHeight")
            print(f"Scrolling {i+1}/{scroll_count} by {viewport_height}px (1x viewport height)...")

            # Scroll down by the full viewport height
            await page.evaluate(f"window.scrollBy(0, {viewport_height})")
            await asyncio.sleep(3)  # Wait for the page to load new products

        # After scrolling, query for all the products and their prices
        try:
            products = await page.query_selector_all("h3.wd-entities-title a")
            original_prices = await page.query_selector_all("div.wrap-price del .woocommerce-Price-amount")
            current_prices = await page.query_selector_all("div.wrap-price ins .woocommerce-Price-amount")

            # Iterate through products and prices, and extract the required information
            for product, original_price, current_price in zip(products, original_prices, current_prices):
                try:
                    product_name = await product.inner_text()
                    original_price_text = await original_price.inner_text()
                    current_price_text = await current_price.inner_text()

                    # Clean up the price text
                    original_price_cleaned = original_price_text.replace("৳", "").replace(",", "").strip()
                    current_price_cleaned = current_price_text.replace("৳", "").replace(",", "").strip()

                    # Add product only if it's not seen already
                    if product_name not in seen_products:
                        seen_products.add(product_name)

                        # Store the product data in a dictionary
                        products_list.append({
                            "product_name": product_name,
                            "current_price": current_price_cleaned,
                            "original_price": original_price_cleaned
                        })

                except Exception as e:
                    print(f"Error extracting product data: {e}")

        except Exception as e:
            print(f"Error querying product elements: {e}")

        # Save the collected data to a JSON file
        file_name = input("Enter the name of the file to save data (e.g., 'products.json'): ")
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(products_list, json_file, ensure_ascii=False, indent=4)

        # Close the browser
        await browser.close()

    # Print the collected product names and prices
    print("Collected product names and prices:", products_list)

# Function to run the asyncio event loop
def main():
    asyncio.run(run_playwright())

if __name__ == "__main__":
    main()
