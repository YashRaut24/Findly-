import os
import urllib.parse
import requests
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
from ddgs import DDGS

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class ResourceFinder:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_search_query(self, user_question: str) -> str:
        """Generate a search query, biased toward technical/programming context."""
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are generating a search query for a TECHNICAL/PROGRAMMING "
                        "search assistant. Always interpret ambiguous terms in a "
                        "software/AI/CS context (e.g. 'RAG' means Retrieval Augmented "
                        "Generation, NOT clothing material). "
                        "Return ONLY the search query, nothing else."
                    )
                },
                {"role": "user", "content": user_question}
            ],
            temperature=0.2,
            max_tokens=30
        )
        return response.choices[0].message.content.strip()

    def get_official_docs_link(self, user_question: str) -> str | None:
        """Ask the LLM if there's a known official documentation site for this topic."""
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "If the user's question is about a specific known programming "
                        "language, library, or framework, respond with ONLY the official "
                        "documentation homepage URL (e.g. https://docs.python.org for Python). "
                        "If there is no clear official docs site, respond with exactly: NONE"
                    )
                },
                {"role": "user", "content": user_question}
            ],
            temperature=0,
            max_tokens=30
        )
        result = response.choices[0].message.content.strip()
        return None if result == "NONE" else result

    def get_youtube_video(self, search_query: str) -> dict:
        """Get an actual specific video using YouTube Data API. Falls back to search page if no API key."""
        if not YOUTUBE_API_KEY:
            encoded = urllib.parse.quote(search_query)
            return {
                "url": f"https://www.youtube.com/results?search_query={encoded}",
                "is_direct_video": False
            }

        try:
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": search_query,
                    "type": "video",
                    "maxResults": 1,
                    "key": YOUTUBE_API_KEY
                },
                timeout=5
            )
            data = response.json()
            video_id = data["items"][0]["id"]["videoId"]
            title = data["items"][0]["snippet"]["title"]
            return {
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "is_direct_video": True
            }
        except Exception:
            encoded = urllib.parse.quote(search_query)
            return {
                "url": f"https://www.youtube.com/results?search_query={encoded}",
                "is_direct_video": False
            }
        

    def get_top_websites(self, search_query: str, max_results: int = 10) -> list[dict]:
        """Get top website results using DuckDuckGo — no API key needed."""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(search_query, max_results=max_results)
                return [
                    {"title": r["title"], "url": r["href"]}
                    for r in results
                ]
        except Exception:
            return []

    def get_external_resources(self, user_question: str) -> dict:
        search_query = self.generate_search_query(user_question)
        encoded_query = urllib.parse.quote(search_query)

        youtube = self.get_youtube_video(search_query)
        docs_link = self.get_official_docs_link(user_question)
        websites = self.get_top_websites(search_query)

        return {
            "search_query_used": search_query,
            "youtube": youtube,
            "official_docs": docs_link,
            "websites": websites,
            "google_ai_mode": f"https://www.google.com/search?q={encoded_query}&udm=50"
        }
    
