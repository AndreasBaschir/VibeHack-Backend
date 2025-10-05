from playwright.async_api import async_playwright, Error as PlaywrightError


async def scrape_website(url):
    """
    Scrape website content using Playwright with optimizations for speed and reliability.

    :param url: The URL of the website to scrape
    :type url: str
    :return: Scraped data including html, title, and other elements.
    :rtype: dict
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set a realistic User-Agent
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Block unnecessary resources to speed up page load
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())

        try:
            print(f"Navigating to {url}...")
            # Use 'domcontentloaded' and a longer timeout for reliability
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)

            html = await page.content()
            title = await page.title()

            # You can add more scraping logic here if needed
            # For example, extracting headings, links, etc.

            return {
                'html': html,
                'title': title,
                # 'headings': headings, ...
            }

        except PlaywrightError as error:
            # If it still fails, raise a specific exception to be handled by the main app
            print(f"Error scraping {url}: {str(error)}")
            raise Exception(f"Failed to scrape website: {error.message}")

        finally:
            await browser.close()