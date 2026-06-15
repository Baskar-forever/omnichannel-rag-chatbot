import re


class ContentCleaner:
    """
    Text normalization only.

    Do NOT:
    - Remove phone numbers
    - Remove emails
    - Remove addresses
    - Remove footer text

    Those should be handled during HTML extraction.
    """

    def clean(
        self,
        text: str
    ) -> str:

        if not text:
            return ""

        cleaned = text

        # Replace non-breaking spaces
        cleaned = cleaned.replace("\xa0", " ")

        # Replace tabs
        cleaned = cleaned.replace("\t", " ")

        # Normalize line endings
        cleaned = cleaned.replace("\r\n", "\n")
        cleaned = cleaned.replace("\r", "\n")

        # Collapse multiple spaces
        cleaned = re.sub(
            r"[ ]{2,}",
            " ",
            cleaned
        )

        # Collapse excessive blank lines
        cleaned = re.sub(
            r"\n{3,}",
            "\n\n",
            cleaned
        )

        # Remove trailing spaces on lines
        cleaned = "\n".join(
            line.strip()
            for line in cleaned.splitlines()
        )

        # Remove repeated punctuation
        cleaned = re.sub(
            r"\.{4,}",
            "...",
            cleaned
        )

        return cleaned.strip()