from bs4 import BeautifulSoup

import requests
import json
from argparse import ArgumentParser

def filter_results(result):
    return result.get("marketing_type") is None
    
def get_best_tab(results):
    results = list(filter(filter_results, results))
    results.sort(key=lambda r: r["votes"])
    return results[-1]

def get_tab_url_from_search(search):
    search = "%20".join(search.split(" "))
    url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={search}"
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    content = json.loads(soup.find(lambda t: t.has_attr("data-content"))["data-content"])
    results = content["store"]["page"]["data"]["results"]
    tab = get_best_tab(results)
    
    return tab["tab_url"]

def get_tab(tab_url):
    soup = BeautifulSoup(requests.get(tab_url).content, 'html.parser')
    content = json.loads(soup.find(lambda t: t.has_attr("data-content"))["data-content"])
    tab = content["store"]["page"]["data"]["tab_view"]
    return {
        "tab": tab["wiki_tab"]["content"],
        # "difficulty": tab["meta"]["difficulty"],
        # "tuning": tab["meta"]["tuning"]["name"],
        # "tuning_value": tab["meta"]["tuning"]["value"],
        # "capo": tab["meta"].get("capo", 0)
    }
    
if __name__ == "__main__":
    parser = ArgumentParser("Get Tab from UG.")
    parser.add_argument("--search", help="Search string", required=True)
    args = parser.parse_args()

    if args.search:
        tab_url = get_tab_url_from_search(args.search)
        print(tab_url)
        tab = get_tab(tab_url)
        print(tab)
