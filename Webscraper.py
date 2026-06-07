# ------------------- IMPORT STATEMENTS -------------------#
import cloudscraper
import json
import Helpers
import Database
from bs4 import BeautifulSoup
import Notifications

# ------------------- MAIN PROGRAM -------------------#
scraper = cloudscraper.create_scraper()


def scrapeAll():
    with open("fragranceBuy-Sites.txt", "r") as file:
        # Read in every "https://fragrancebuy.ca/products/" link from the .txt file
        for line in file:
            if line.startswith("https://fragrancebuy.ca/products/"):
                url, variantID = Helpers.parseUrl(
                    line.strip()
                )  # Parse the url to get the json and specific variant ID (Distinguish between options)
                response = scraper.get(url)

                if (
                    response.status_code == 200
                ):  # If the site is able to be accessed, then scrape, otherwise skip it
                    response = (
                        response.json()
                    )  # Convert site contents to .json format to access data
                    variants = response["product"]["variants"]

                    if (
                        variantID is None
                    ):  # Determine the specific variant of the fragrance that was specified in the link (100 ml, 50 ml, refurbished, etc...)
                        location = response["product"]["variants"][0]
                    else:
                        for subfolder in variants:
                            if subfolder["id"] == variantID:
                                location = subfolder

                    # Scrape all of the data required
                    title = str(location["title"])
                    current_price = float(location["price"])
                    quantity = int(location["inventory_quantity"])
                    img = response["product"]["image"]["src"]

                    # print(title)

                    oldPrice = Database.getLatestPrice(title=title)
                    oldQuantity = Database.getLatestQuantity(title=title)

                    if current_price > oldPrice:
                        # Notify User that Price has increased
                        Notifications.priceIncrease(
                            title=title,
                            newPrice=current_price,
                            oldPrice=oldPrice,
                            imgLink=img,
                            productLink=line.strip(),
                        )

                    elif current_price < oldPrice:
                        # Notify User that Price has decreased
                        Notifications.priceDecrease(
                            title=title,
                            newPrice=current_price,
                            oldPrice=oldPrice,
                            imgLink=img,
                            productLink=line.strip(),
                        )

                    if quantity > oldQuantity:
                        # Notify user that stock has increased
                        Notifications.quantityIncrease(
                            title=title,
                            newQuantity=quantity,
                            oldQuantity=oldQuantity,
                            imgLink=img,
                            productLink=line.strip(),
                        )
                    elif quantity < oldQuantity:
                        # Notify user that stock has decreased
                        Notifications.quantityDecrease(
                            title=title,
                            newQuantity=quantity,
                            oldQuantity=oldQuantity,
                            imgLink=img,
                            productLink=line.strip(),
                        )

                    # Add those data points to the table of the specific cologne
                    Database.setDB(title, current_price, quantity, line.strip())

                else:
                    print("\n#-----------------------#")
                    print("UNABLE TO REACH SITE")
                    print(f"Site URL: {url}")
                    print(f"Error code: {response.status_code}")
                    print("Skipping this site...")
                    print("#-----------------------#\n")
    print("Done Scraping")
    scraper.close()


# Scrape One SQL Store
def scrapeOne(product: str):
    url, variantID = Helpers.parseUrl(
        url=product.strip()
    )  # Parse the url to get the json and specific variant ID (Distinguish between options)
    response = scraper.get(url)

    if (
        response.status_code == 200
    ):  # If the site is able to be accessed, then scrape, otherwise skip it
        response = (
            response.json()
        )  # Convert site contents to .json format to access data
        variants = response["product"]["variants"]

        if (
            variantID is None
        ):  # Determine the specific variant of the fragrance that was specified in the link (100 ml, 50 ml, refurbished, etc...)
            location = response["product"]["variants"][0]
        else:
            for subfolder in variants:
                if subfolder["id"] == variantID:
                    location = subfolder

        # Scrape all of the data required
        title = str(location["title"])
        current_price = float(location["price"])
        offsalePrice = location["compare_at_price"]
        quantity = int(location["inventory_quantity"])

        # Add those data points to the table of the specific cologne
        Database.setDB(title, current_price, quantity, product)

    print("Done Scraping One")
    scraper.close()


def scrapeLiveData(url):
    url, variantID = Helpers.parseUrl(
        url=url.strip()
    )  # Parse the url to get the json and specific variant ID (Distinguish between options)
    response = scraper.get(url)

    if (
        response.status_code == 200
    ):  # If the site is able to be accessed, then scrape, otherwise skip it
        response = (
            response.json()
        )  # Convert site contents to .json format to access data
        variants = response["product"]["variants"]

        if (
            variantID is None
        ):  # Determine the specific variant of the fragrance that was specified in the link (100 ml, 50 ml, refurbished, etc...)
            location = response["product"]["variants"][0]
        else:
            for subfolder in variants:
                if subfolder["id"] == variantID:
                    location = subfolder
                    break

        # Scrape all of the data required
        current_price = float(location["price"])
        current_quantity = int(location["inventory_quantity"])
        regular_price = location["compare_at_price"]
        description = str(response["product"]["body_html"])

        description = (
            description.replace("</p>", "").replace("<br>", "").replace("<p>", "")
        )

        img = response["product"]["image"]["src"]

        if regular_price == "":
            regular_price = None
        else:
            regular_price = float(regular_price)

        return (current_price, current_quantity, regular_price, description, img)


if __name__ == "__main__":
    scrapeAll()
