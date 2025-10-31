# visualizer.py
"""
Visualization module for Dream Journal Analyzer.
Creates embedded matplotlib charts for Tkinter integration.
"""

try:
    import matplotlib

    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.dates as mdates
    from datetime import datetime
    from collections import Counter

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class DreamVisualizer:
    """Handles creation of embedded visualizations for dream data."""

    def __init__(self, journal):
        self.journal = journal

    @staticmethod
    def is_available():
        """Check if matplotlib is available."""
        return MATPLOTLIB_AVAILABLE

    def create_mood_timeline(self, parent_frame):
        """
        Creates an embedded mood timeline chart in the given Tkinter frame.

        Args:
            parent_frame: Tkinter frame to embed the chart in

        Returns:
            Canvas widget if successful, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        # Extract dates and mood scores
        dates = []
        scores = []

        for dream in self.journal.dreams:
            if dream.mood_score is not None:
                try:
                    date_obj = datetime.strptime(dream.date, "%Y-%m-%d")
                    dates.append(date_obj)
                    scores.append(dream.mood_score)
                except ValueError:
                    continue

        if not dates:
            return None

        # Sort by date to ensure proper timeline
        sorted_data = sorted(zip(dates, scores))
        dates, scores = zip(*sorted_data)

        # Create figure
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Plot mood timeline with dotted line
        ax.plot(dates, scores, marker='o', linewidth=2.5,
                markersize=10, color='#2196F3', label='Mood Score',
                markeredgecolor='white', markeredgewidth=2, alpha=0.9,
                dash_capstyle='round')

        # Add horizontal reference lines with better styling
        ax.axhline(y=0.5, color='#4CAF50', linestyle='--', alpha=0.5, linewidth=1.5,
                   label='Very Positive (+0.5)')
        ax.axhline(y=0, color='#9E9E9E', linestyle='--', alpha=0.5, linewidth=1.5,
                   label='Neutral (0)')
        ax.axhline(y=-0.5, color='#F44336', linestyle='--', alpha=0.5, linewidth=1.5,
                   label='Very Negative (-0.5)')

        # Fill areas between thresholds for better visualization
        ax.axhspan(0.5, 1.0, alpha=0.1, color='green', zorder=0)
        ax.axhspan(0.1, 0.5, alpha=0.05, color='lightgreen', zorder=0)
        ax.axhspan(-0.1, 0.1, alpha=0.05, color='gray', zorder=0)
        ax.axhspan(-0.5, -0.1, alpha=0.05, color='lightcoral', zorder=0)
        ax.axhspan(-1.0, -0.5, alpha=0.1, color='red', zorder=0)

        # Styling
        ax.set_xlabel('Date', fontsize=11, fontweight='bold', labelpad=10)
        ax.set_ylabel('Mood Score', fontsize=11, fontweight='bold', labelpad=10)
        ax.set_title('Dream Mood Timeline', fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.2, linestyle=':', linewidth=1)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        ax.set_ylim(-1.1, 1.1)

        # Format dates on x-axis
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))

        # Rotate date labels for better readability
        fig.autofmt_xdate(rotation=30, ha='right')

        # Add padding and tight layout
        fig.tight_layout(pad=2.0)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()

    def create_mood_distribution(self, parent_frame):
        """
        Creates an embedded mood distribution bar chart in the given Tkinter frame.

        Args:
            parent_frame: Tkinter frame to embed the chart in

        Returns:
            Canvas widget if successful, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        # Count dreams in each category
        categories = {
            'Very Positive': 0,
            'Positive': 0,
            'Neutral': 0,
            'Negative': 0,
            'Very Negative': 0
        }

        for dream in self.journal.dreams:
            if dream.mood_score is not None:
                score = dream.mood_score
                if score >= 0.5:
                    categories['Very Positive'] += 1
                elif score >= 0.1:
                    categories['Positive'] += 1
                elif score >= -0.1:
                    categories['Neutral'] += 1
                elif score >= -0.5:
                    categories['Negative'] += 1
                else:
                    categories['Very Negative'] += 1

        # Create figure
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
        bars = ax.bar(categories.keys(), categories.values(), color=colors, alpha=0.8)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold')

        # Styling
        ax.set_xlabel('Mood Category', fontsize=10, fontweight='bold')
        ax.set_ylabel('Number of Dreams', fontsize=10, fontweight='bold')
        ax.set_title('Dream Mood Distribution', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        fig.autofmt_xdate()
        fig.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()

    def create_themes_chart(self, parent_frame, top_n=15):
        """
        Creates an embedded top themes horizontal bar chart in the given Tkinter frame.

        Args:
            parent_frame: Tkinter frame to embed the chart in
            top_n: Number of top themes to display

        Returns:
            Canvas widget if successful, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        # Extract all words
        all_words = []
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'can', 'am', 'is', 'are', 'i', 'me', 'my', 'you', 'your', 'it', 'its'
        }

        for dream in self.journal.dreams:
            words = dream.text.lower().split()
            filtered = [w.strip('.,!?;:()[]{}""\'') for w in words
                        if w.isalpha() and len(w) > 2 and w not in stop_words]
            all_words.extend(filtered)

        if not all_words:
            return None

        # Get top themes
        word_counts = Counter(all_words)
        top_themes = word_counts.most_common(top_n)

        themes = [theme for theme, count in reversed(top_themes)]
        counts = [count for theme, count in reversed(top_themes)]

        # Create figure
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        bars = ax.barh(themes, counts, color='#2196F3', alpha=0.7)

        # Color bars based on frequency (gradient effect)
        max_count = max(counts) if counts else 1
        for i, bar in enumerate(bars):
            intensity = counts[i] / max_count
            bar.set_color(matplotlib.cm.Blues(0.4 + intensity * 0.6))

        # Styling
        ax.set_xlabel('Frequency', fontsize=10, fontweight='bold')
        ax.set_ylabel('Theme', fontsize=10, fontweight='bold')
        ax.set_title(f'Top {top_n} Recurring Dream Themes', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        fig.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()

    def get_statistics_summary(self):
        """
        Returns a dictionary of visualization statistics.

        Returns:
            Dictionary with visualization data or None if no data
        """
        if not self.journal.dreams:
            return None

        # Count mood categories
        mood_counts = {
            'Very Positive': 0,
            'Positive': 0,
            'Neutral': 0,
            'Negative': 0,
            'Very Negative': 0
        }

        for dream in self.journal.dreams:
            if dream.mood_score is not None:
                score = dream.mood_score
                if score >= 0.5:
                    mood_counts['Very Positive'] += 1
                elif score >= 0.1:
                    mood_counts['Positive'] += 1
                elif score >= -0.1:
                    mood_counts['Neutral'] += 1
                elif score >= -0.5:
                    mood_counts['Negative'] += 1
                else:
                    mood_counts['Very Negative'] += 1

        return {
            'total_dreams': len(self.journal.dreams),
            'mood_distribution': mood_counts,
            'has_mood_scores': any(d.mood_score is not None for d in self.journal.dreams)
        }
