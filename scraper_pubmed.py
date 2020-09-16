import json

import requests
from bs4 import BeautifulSoup


def get_results():
    key = 'Covid-19'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    base_url = f"https://pubmed.ncbi.nlm.nih.gov"
    url = f"{base_url}/?term={key}&size=50"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html')
    results = []
    for item in soup.find_all("a", class_="docsum-title"):
        link = f"{base_url}{item.attrs['href']}"
        article = BeautifulSoup(requests.get(link, headers=headers).text, 'html')
        title = article.find('h1', class_="heading-title").text.strip()
        print(link)
        print(title)
        abstract = article.find(id="enc-abstract")
        if abstract:
            abstract = abstract.text.strip()
        else:
            abstract = ""
        results.append({"title": title, "abstract": abstract})
    return results


def store_result(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    store_result(get_results())
