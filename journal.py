# journal.py
import json
import os
from dream import Dream


class DreamJournal:
    """Handles file I/O and storage of Dream objects."""

    def __init__(self, filename="dreams.json"):
        self.filename = filename
        self.dreams = self.load_dreams()

    def load_dreams(self):
        """Loads dreams from file with error handling."""
        if not os.path.exists(self.filename):
            print(f"No existing journal found. Creating new file: {self.filename}")
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Validate data structure
                if not isinstance(data, list):
                    print("Invalid journal format. Resetting...")
                    self.reset_file()
                    return []

                dreams = []
                for entry in data:
                    try:
                        dreams.append(Dream.from_dict(entry))
                    except (KeyError, TypeError) as e:
                        print(f"Skipping corrupted dream entry: {e}")
                        continue

                return dreams

        except json.JSONDecodeError as e:
            print(f"Corrupted JSON file detected: {e}")
            # Backup corrupted file
            backup_name = f"{self.filename}.backup"
            try:
                os.rename(self.filename, backup_name)
                print(f"Corrupted file backed up to: {backup_name}")
            except Exception:
                pass

            self.reset_file()
            return []

        except Exception as e:
            print(f"Unexpected error loading dreams: {e}")
            return []

    def save_dreams(self):
        """Saves dreams to file with error handling."""
        try:
            # Create temporary file first
            temp_filename = f"{self.filename}.tmp"

            with open(temp_filename, "w", encoding="utf-8") as f:
                json.dump([d.to_dict() for d in self.dreams], f, indent=2, ensure_ascii=False)

            # Replace original file only if write succeeded
            if os.path.exists(self.filename):
                os.replace(temp_filename, self.filename)
            else:
                os.rename(temp_filename, self.filename)

        except Exception as e:
            print(f"Error saving dreams: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except Exception:
                    pass

    def add_dream(self, dream):
        """Adds a dream to the journal."""
        if not isinstance(dream, Dream):
            raise TypeError("Only Dream objects can be added to the journal")

        self.dreams.append(dream)
        self.save_dreams()

    def reset_file(self):
        """Clears the journal file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)
            print(f"Journal file reset: {self.filename}")
        except Exception as e:
            print(f"Error resetting file: {e}")

    def get_dream_count(self):
        """Returns the total number of dreams."""
        return len(self.dreams)

    def get_dreams_by_date(self, date_str):
        """Returns all dreams from a specific date."""
        return [d for d in self.dreams if d.date == date_str]

    def delete_dream(self, index):
        """Deletes a dream by index."""
        if 0 <= index < len(self.dreams):
            deleted = self.dreams.pop(index)
            self.save_dreams()
            return deleted
        return None
