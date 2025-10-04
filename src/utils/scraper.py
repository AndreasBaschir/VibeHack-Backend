from playwright.async_api import async_playwright


async def scrape_website(url):
    """
    Scrape website content using Playwright

    :param url: The URL of the website to scrape
    :type url: str
    :return: Scraped data including html, title, headings, links, images, and paragraphs
    :rtype: dict
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until='networkidle')

            # Get HTML content
            html = await page.content()

            # Extract common website data
            data = await page.evaluate("""
                () => {
                    return {
                        title: document.title,
                        headings: Array.from(document.querySelectorAll('h1, h2, h3'))
                            .map(el => ({ tag: el.tagName, text: el.textContent.trim() })),
                        links: Array.from(document.querySelectorAll('a'))
                            .map(el => ({ text: el.textContent.trim(), href: el.href }))
                            .filter(link => link.href),
                        images: Array.from(document.querySelectorAll('img'))
                            .map(el => ({ alt: el.alt, src: el.src })),
                        paragraphs: Array.from(document.querySelectorAll('p'))
                            .map(el => el.textContent.trim())
                            .filter(text => text.length > 0)
                    };
                }
            """)

            # Add HTML to the returned data
            data['html'] = html

            return data
        except Exception as error:
            print(f'Error scraping website: {error}')
        finally:
            await browser.close()
