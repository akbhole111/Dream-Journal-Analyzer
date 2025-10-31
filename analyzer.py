# analyzer.py
from collections import Counter
import os


class DreamAnalyzer:
    """Analyzes dream content using VADER sentiment and keyword frequency."""

    def __init__(self, journal):
        self.journal = journal
        self.sia = None
        self._initialize_sentiment_analyzer()

    def _initialize_sentiment_analyzer(self):
        """Initialize VADER sentiment analyzer with proper setup."""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            from nltk import data as nltk_data

            # Check if vader_lexicon is already downloaded
            try:
                nltk_data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                # Download only if not found
                from nltk import download
                print("Downloading VADER lexicon (one-time setup)...")
                download("vader_lexicon", quiet=True)

            self.sia = SentimentIntensityAnalyzer()

        except Exception as e:
            print(f"Error initializing sentiment analyzer: {e}")
            self.sia = None

    def analyze(self):
        """Performs comprehensive dream analysis."""
        if not self.journal.dreams:
            return "No dreams to analyze. Start recording your dreams!"

        if self.sia is None:
            return "Sentiment analyzer not available. Please check NLTK installation."

        mood_scores = []
        all_words = []

        # Common stop words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
            't', 'can', 'will', 'just', 'don', 'should', 'now', 'was', 'were',
            'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
            'doing', 'am', 'is', 'are', 'be', 'as', 'i', 'me', 'my', 'myself',
            'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
            'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
            'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
            'those', 'if', 'because', 'while', 'out', 'off', 'over', 'down'
        }

        for dream in self.journal.dreams:
            # Calculate sentiment score
            score = self.sia.polarity_scores(dream.text)["compound"]
            dream.mood_score = score
            mood_scores.append(score)

            # Extract meaningful words
            words = dream.text.lower().split()
            filtered_words = [
                word.strip('.,!?;:()[]{}""\'')
                for word in words
                if word.isalpha() and len(word) > 2 and word.lower() not in stop_words
            ]
            all_words.extend(filtered_words)

        # Save updated mood scores
        self.journal.save_dreams()

        # Calculate statistics
        avg_score = sum(mood_scores) / len(mood_scores) if mood_scores else 0

        # Get top themes using Counter
        word_counts = Counter(all_words)
        top_themes = [word for word, count in word_counts.most_common(10)]

        # ADVANCED: Create mood distribution matrix (multidimensional array)
        mood_matrix = self._create_mood_distribution_matrix(mood_scores)

        return {
            "total_dreams": len(self.journal.dreams),
            "average_mood": round(avg_score, 3),
            "top_themes": top_themes,
            "mood_matrix": mood_matrix,
        }

    def _create_mood_distribution_matrix(self, mood_scores):
        """
        ADVANCED TOPIC: Multidimensional Arrays
        Creates a 2D matrix categorizing dreams by mood ranges and time periods.

        Matrix structure:
        Rows: Mood categories (Very Negative, Negative, Neutral, Positive, Very Positive)
        Columns: [Count, Min Score, Max Score, Average Score]
        """
        # Initialize 5x4 matrix (5 mood categories x 4 statistics)
        mood_matrix = [
            [0, 1.0, -1.0, 0.0],  # Very Positive: count, min, max, avg
            [0, 1.0, -1.0, 0.0],  # Positive
            [0, 1.0, -1.0, 0.0],  # Neutral
            [0, 1.0, -1.0, 0.0],  # Negative
            [0, 1.0, -1.0, 0.0],  # Very Negative
        ]

        category_scores = [[], [], [], [], []]  # Store scores for each category

        for score in mood_scores:
            # Determine category index using recursive categorization
            category_idx = self._categorize_mood_recursive(score, 0)

            # Update matrix: [count, min, max, sum_for_avg]
            mood_matrix[category_idx][0] += 1  # Increment count
            category_scores[category_idx].append(score)

        # Calculate min, max, avg for each category
        for i in range(5):
            if category_scores[i]:
                mood_matrix[i][1] = min(category_scores[i])  # Min
                mood_matrix[i][2] = max(category_scores[i])  # Max
                mood_matrix[i][3] = sum(category_scores[i]) / len(category_scores[i])  # Avg

        return mood_matrix

    def _categorize_mood_recursive(self, score, depth=0, max_depth=10):
        """
        ADVANCED TOPIC: Recursion
        Recursively categorizes a mood score into one of 5 categories.
        Uses recursion with depth limiting to demonstrate the concept.

        Returns category index: 0=Very Positive, 1=Positive, 2=Neutral,
                                3=Negative, 4=Very Negative
        """
        # Base case: max depth reached or score categorized
        if depth >= max_depth:
            return 2  # Default to neutral

        # Recursive categorization with boundary checking
        if score >= 0.5:
            return 0  # Very Positive
        elif score >= 0.1:
            # Recursively verify it's in positive range
            if self._is_in_range_recursive(score, 0.1, 0.5, depth + 1):
                return 1  # Positive
        elif score >= -0.1:
            return 2  # Neutral
        elif score >= -0.5:
            # Recursively verify it's in negative range
            if self._is_in_range_recursive(score, -0.5, -0.1, depth + 1):
                return 3  # Negative
        else:
            return 4  # Very Negative

        # Fallback recursive call
        return self._categorize_mood_recursive(score, depth + 1)

    def _is_in_range_recursive(self, value, min_val, max_val, depth=0, max_depth=5):
        """
        ADVANCED TOPIC: Recursion (Helper)
        Recursively checks if a value is within a range.
        Demonstrates recursive boundary checking.
        """
        # Base case
        if depth >= max_depth:
            return min_val <= value < max_val

        # Recursive case: check boundaries step by step
        if value < min_val:
            return False
        elif value >= max_val:
            return False
        else:
            # Recursively confirm with increased depth
            return self._is_in_range_recursive(value, min_val, max_val, depth + 1)

    def get_mood_distribution_summary(self):
        """Returns a formatted summary of the mood distribution matrix."""
        result = self.analyze()
        if isinstance(result, str):
            return result

        mood_matrix = result.get('mood_matrix', [])
        categories = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']

        summary = "\nMood Distribution Matrix:\n"
        summary += f"{'Category':<15} {'Count':<8} {'Min':<8} {'Max':<8} {'Avg':<8}\n"
        summary += "=" * 55 + "\n"

        for i, category in enumerate(categories):
            if mood_matrix[i][0] > 0:  # Only show categories with dreams
                summary += f"{category:<15} {mood_matrix[i][0]:<8} "
                summary += f"{mood_matrix[i][1]:<8.3f} {mood_matrix[i][2]:<8.3f} "
                summary += f"{mood_matrix[i][3]:<8.3f}\n"

        return summary
