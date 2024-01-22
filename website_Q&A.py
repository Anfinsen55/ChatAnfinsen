import requests
from bs4 import BeautifulSoup

def answer_question_from_website_or_search(url, question):
    """Retrieves relevant information from the specified website or Google Search to answer the user's question."""

    try:
        if url:
            # Use BeautifulSoup for direct website parsing
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Customize this logic for specific websites and question types
            relevant_elements = soup.find_all(text=lambda text: question.lower() in text.lower())
            answer = " ".join(element.parent.text.strip() for element in relevant_elements)

        else:
            # Use Google Search API for broader search
            api_key = "AIzaSyDdIimoQuikBlidQlPLScVPH3x2UTfbCHM"  # Replace with your API key
            query = f"site:{url} {question}"
            search_url = f"https://www.protectedtext.com/aj_tell_me_about_yourself={api_key}&cx=017576662512468239146:dau7l0ei6yk&q={query}"
            response = requests.get(search_url)
            response.raise_for_status()

            # Parse JSON response and extract relevant information (customize as needed)
            data = response.json()
            answer = " ".join(item["snippet"] for item in data["items"])

    except requests.exceptions.RequestException as e:
        return f"Error accessing the website or search results: {e}"

    except ValueError:
        return "Unable to process the website or search results."

    return answer

# ... rest of the code (user prompts, input handling, etc.) ...
