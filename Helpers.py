import cloudscraper

scraper = cloudscraper.create_scraper()


# Take the url, chop off the end, and and .js to it
def parseUrl(url: str):
    # https://fragrancebuy.ca/products/fomoeclatnoir-man?variant=42757886181438
    # TO
    # https://fragrancebuy.ca/products/fomoeclatnoir-man.json

    variantID = None

    if "?variant=" in url:
        index = url.index("?variant=")
        variantID = url[index + 9 : :]
        url = url[0:index] + ".json"

    elif url.endswith(".json"):
        pass
    else:
        url += ".json"

    if variantID is not None:
        variantID = int(variantID)

    return (url, variantID)


def urlValidifier(url) -> bool:

    try:
        response = scraper.get(url)

    except:
        return False

    return response.status_code == 200
