# main.py

from journal import DreamJournal
from ui import DreamUI


def main():
    """Main entry point for the Dream Journal Analyzer."""
    print("=" * 60)
    print("Dream Journal Analyzer - Starting...")
    print("=" * 60)

    # Initialize journal and UI
    journal = DreamJournal("dreams.json")
    ui = DreamUI(journal)

    print(f"Loaded {journal.get_dream_count()} existing dreams.")
    print("GUI window opened!")
    print("=" * 60)

    # Run the application
    ui.run()


if __name__ == "__main__":
    main()
