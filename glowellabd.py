import asyncio
import json
from playwright.async_api import async_playwright

async def run_playwright():
    async with async_playwright() as p:
        # Launch Firefox browser (headless=False for debugging)
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        # Initialize list for products
        all_products = []

        # Pagination loop
        page_number = 1
        while True:
            print(f"Visiting page {page_number}...")
            url = f'https://glowellabd.com/product-category/skin-care/page/{page_number}'
            await page.goto(url)
            # Extract product names and prices
            try:
                products = await page.query_selector_all("h3.wd-entities-title a")
                prices = await page.query_selector_all("span.price")

                print(f"Products found: {len(products)}, Prices found: {len(prices)}")

                for i in range(len(products)):
                    try:
                        # Extract product name
                        product_name = await products[i].inner_text()

                        # Extract current price
                        price_element = prices[i]
                        current_price_element = await price_element.query_selector("ins span.woocommerce-Price-amount")
                        if current_price_element:
                            current_price = await current_price_element.inner_text()
                        else:
                            # Fall back to the standard price
                            current_price_element = await price_element.query_selector("span.woocommerce-Price-amount")
                            current_price = await current_price_element.inner_text()

                        all_products.append({"Product Name": product_name, "Price": current_price})
                    except Exception as e:
                        print(f"Error extracting product or price: {e}")

            except Exception as e:
                print(f"Error querying product elements: {e}")

            # Move to the next page
            page_number += 1

        # Close the browser
        await browser.close()

    # Save data to a JSON file
    if all_products:
        with open("products.json", "w", encoding="utf-8") as json_file:
            json.dump(all_products, json_file, ensure_ascii=False, indent=4)
        print("Data saved to products.json")
    else:
        print("No data to save.")

# Function to run the asyncio event loop
def main():
    asyncio.run(run_playwright())

if __name__ == "__main__":
    main()
