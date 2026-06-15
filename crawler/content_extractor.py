import requests

from bs4 import BeautifulSoup

from app.models.document import Document

class ContentExtractor:

    REMOVE_SELECTORS = [
        "header",
        "footer",
        "nav",
        ".mobile-header",
        ".main-header",
        ".footer",
        ".offcanvas",
        "#myBtn",
        "script",
        "style",
        "noscript",
    ]

    def __init__(
        self,
        timeout: int = 15
    ):
        self.timeout = timeout

    def _enrich_dom(
        self,
        soup: BeautifulSoup
    ) -> BeautifulSoup:
        """
        Replace JS-driven placeholder values
        with actual business values from attributes.
        """

        for counter in soup.select(".counting-number"):

            data_count = counter.get(
                "data-count"
            )

            if data_count:
                counter.string = str(
                    data_count
                )

        return soup

    def extract(
        self,
        url: str
    ) -> Document:

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Enrich dynamic content FIRST
        soup = self._enrich_dom(
            soup
        )

        # Remove unwanted sections
        for selector in self.REMOVE_SELECTORS:

            for element in soup.select(
                selector
            ):
                element.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        body = soup.body or soup

        content = body.get_text(
            separator=" ",
            strip=True
        )

        return Document(
            url=url,
            title=title,
            content=content,
            source="website",
            metadata={}
        )