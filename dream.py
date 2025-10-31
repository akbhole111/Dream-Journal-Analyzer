# dream.py

class Dream:
    """Represents a single dream entry with text, date, and mood score."""

    def __init__(self, text, date, mood_score=None):
        if not text or not isinstance(text, str):
            raise ValueError("Dream text must be a non-empty string")
        if not date or not isinstance(date, str):
            raise ValueError("Dream date must be a non-empty string")

        self.text = text.strip()
        self.date = date
        self.mood_score = mood_score

    def __str__(self):
        """Returns a readable string representation of the dream."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        mood_str = f" (Mood: {self.mood_score:.2f})" if self.mood_score is not None else ""
        return f"{self.date}: {preview}{mood_str}"

    def __repr__(self):
        """Returns a detailed representation for debugging."""
        return f"Dream(date='{self.date}', text_length={len(self.text)}, mood_score={self.mood_score})"

    def to_dict(self):
        """Converts dream object to dictionary for JSON serialization."""
        return {
            "text": self.text,
            "date": self.date,
            "mood_score": self.mood_score
        }

    @staticmethod
    def from_dict(data):
        """Creates a Dream object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")

        required_fields = ["text", "date"]
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Missing required field: {field}")

        return Dream(
            text=data["text"],
            date=data["date"],
            mood_score=data.get("mood_score")
        )

    def get_word_count(self):
        """Returns the word count of the dream text."""
        return len(self.text.split())

    def contains_keyword(self, keyword):
        """Checks if dream contains a specific keyword (case-insensitive)."""
        return keyword.lower() in self.text.lower()
