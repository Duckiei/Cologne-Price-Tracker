# ------------------- IMPORT STATEMENTS -------------------#
import cloudscraper
import Helpers
import Database
import Notifications

# ------------------- MAIN PROGRAM & FUNCTIONS -------------------#
scraper = cloudscraper.create_scraper()


# Scrape data from all links in .txt file
def scrapeAll(scraper=scraper):
    with open("fragranceBuy-Sites.txt", "r") as file:
        # Read in every "https://fragrancebuy.ca/products/" link from the .txt file
        for fragBuyURL in file:
            if fragBuyURL.startswith("https://fragrancebuy.ca/products/"):
                response, location = findDataLocation(fragBuyURL, scraper=scraper)

                if response is None or location is None:
                    continue

                # Scrape all of the data required
                title = str(location["title"])
                current_price = float(location["price"])
                quantity = int(location["inventory_quantity"])
                img = response["product"]["image"]["src"]

                print(title)

                # Find last price and quantity in database
                oldPrice = Database.getLatestPrice(title=title)
                oldQuantity = Database.getLatestQuantity(title=title)

                # Send notification for changes in price and quantity (if applicable)
                if current_price > oldPrice:
                    # Notify User that Price has increased
                    Notifications.priceIncrease(
                        title=title,
                        newPrice=current_price,
                        oldPrice=oldPrice,
                        imgLink=img,
                        productLink=fragBuyURL.strip(),
                    )

                elif current_price < oldPrice:
                    Notifications.priceDecrease(
                        title=title,
                        newPrice=current_price,
                        oldPrice=oldPrice,
                        imgLink=img,
                        productLink=fragBuyURL.strip(),
                    )

                if quantity > oldQuantity:
                    Notifications.quantityIncrease(
                        title=title,
                        newQuantity=quantity,
                        oldQuantity=oldQuantity,
                        imgLink=img,
                        productLink=fragBuyURL.strip(),
                    )
                elif quantity < oldQuantity:
                    Notifications.quantityDecrease(
                        title=title,
                        newQuantity=quantity,
                        oldQuantity=oldQuantity,
                        imgLink=img,
                        productLink=fragBuyURL.strip(),
                    )

                # Add scraped data to database
                Database.setDB(title, current_price, quantity, fragBuyURL.strip())

    print("Finished scraping all links.")
    scraper.close()


# Scrape a single products information, and store in db
def scrapeOne(fragBuyURL, scraper=scraper):
    response, location = findDataLocation(fragBuyURL, scraper=scraper)

    # Scrape all of the data required
    title = str(location["title"])
    current_price = float(location["price"])
    offsalePrice = location["compare_at_price"]
    quantity = int(location["inventory_quantity"])

    # Add those data points to the table of the specific cologne
    Database.setDB(title, current_price, quantity, fragBuyURL)

    print("Finished scraping single link.")
    scraper.close()


# Scrape a single products information, and return it for live usage (no db)
def scrapeLiveData(fragBuyURL, scraper=scraper):
    response, location = findDataLocation(fragBuyURL, scraper=scraper)

    # Scrape all of the data required
    current_price = float(location["price"])
    current_quantity = int(location["inventory_quantity"])
    regular_price = location["compare_at_price"]
    description = str(response["product"]["body_html"])

    description = description.replace("</p>", "").replace("<br>", "").replace("<p>", "")

    img = response["product"]["image"]["src"]

    if regular_price == "":
        regular_price = None
    else:
        regular_price = float(regular_price)

    return (current_price, current_quantity, regular_price, description, img)


def findDataLocation(url, scraper=scraper):
    # Parse the url to get the json and specific variant ID (Distinguish between options)
    fragBuyJSONURL, variantID = Helpers.parseUrl(url.strip())

    response = scraper.get(fragBuyJSONURL)

    # If the site is able to be accessed, then scrape, otherwise skip it
    if response.status_code == 200:
        # Convert site contents to .json format to access data
        response = response.json()

        # Access the list that contains all the variants in the json file
        variants = response["product"]["variants"]

        # No variant ID = Single variant in the list (access it directly)
        if variantID is None:
            location = response["product"]["variants"][0]

        # If there is a variant ID, iterate through all the variants to match up ID to find right one
        else:
            for variant in variants:
                if variant["id"] == variantID:
                    location = variant
                    break
        return response, location
    else:
        print(f'Unable to scrape data from: "{fragBuyJSONURL}"')
        print(f'Response code: "{response.status_code}"')
        return None, None


if __name__ == "__main__":
    scrapeAll()
