import requests
from bs4 import BeautifulSoup

STACK_APP_KEY = "API-KEY-HERE"  # Replace with your StackExchange API key

def search_stackoverflow(query):
    """
    Search Stack Overflow using StackExchange API with FIXR's app key.
    Returns the question ID and URL of the top result.
    """
    url = "https://api.stackexchange.com/2.3/search"
    params = {
        "order": "desc",
        "sort": "relevance",
        "intitle": query,
        "site": "stackoverflow",
        "pagesize": 1,
        "key": STACK_APP_KEY
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if items:
        return items[0]["question_id"], items[0]["link"]
    return None, None


def get_top_answer(question_id):
    """
    Fetch the top answer for a Stack Overflow question by ID.
    Returns the plain text from the HTML body.
    """
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",
        "pagesize": 1,
        "key": STACK_APP_KEY
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    answers = resp.json().get("items", [])
    if not answers:
        return None
    html = answers[0]["body"]
    return BeautifulSoup(html, "html.parser").get_text()


def main():
    print("🔎 FIXR Stack Overflow Answer Fetcher (App-Key Auth)\n")
    while True:
        query = input("Enter your issue (or type 'exit'): ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break
        if not query:
            continue

        print("🔍 Searching Stack Overflow...")
        qid, link = search_stackoverflow(query)
        if not qid:
            print("❌ No matching question found.\n")
            continue

        print(f"🔗 Found: {link}\n\n📄 Fetching top answer...\n")
        answer_text = get_top_answer(qid)
        if answer_text:
            print("🟢 TOP ANSWER:\n")
            print(answer_text.strip())
        else:
            print("❌ No answer found.")

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
