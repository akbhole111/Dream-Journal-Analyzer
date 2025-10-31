# ui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dream import Dream
from analyzer import DreamAnalyzer
from datetime import date, datetime

# Try to import visualizer
try:
    from visualizer import DreamVisualizer

    VISUALIZER_AVAILABLE = DreamVisualizer.is_available()
except ImportError:
    VISUALIZER_AVAILABLE = False


class DreamUI:
    """Enhanced Tkinter UI for dream journaling with embedded visualizations."""

    def __init__(self, journal):
        self.journal = journal
        self.visualizer = DreamVisualizer(journal) if VISUALIZER_AVAILABLE else None
        self.root = tk.Tk()
        self.root.title("Dream Journal Analyzer")
        self.root.geometry("1400x700")
        self.root.resizable(True, True)

        # Main container
        main_container = tk.Frame(self.root, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create two-column layout
        # Left side - Input (25% width)
        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_frame.config(width=300)

        # Right side - Results and Visualization (75% width)
        right_frame = tk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        # ===== LEFT SIDE - INPUT =====
        tk.Label(left_frame, text="✍️ Record Dream",
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        # Date selection
        date_frame = tk.Frame(left_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(date_frame, text="Date:", font=("Arial", 9)).pack(anchor=tk.W)
        self.date_entry = tk.Entry(date_frame, width=25, font=("Arial", 10))
        self.date_entry.insert(0, str(date.today()))
        self.date_entry.pack(fill=tk.X, pady=(2, 0))
        tk.Label(date_frame, text="(YYYY-MM-DD)", fg="gray", font=("Arial", 8)).pack(anchor=tk.W)

        # Dream entry
        tk.Label(left_frame, text="Dream Description:",
                 font=("Arial", 9)).pack(anchor=tk.W, pady=(15, 5))

        text_frame = tk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_entry = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10),
                                  height=10)
        text_scrollbar = tk.Scrollbar(text_frame, command=self.text_entry.yview)
        self.text_entry.config(yscrollcommand=text_scrollbar.set)

        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=15, fill=tk.X)

        tk.Button(button_frame, text="Add Dream", command=self.add_dream,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  pady=8).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Analyze Dreams", command=self.show_analysis,
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                  pady=8).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="View All Dreams", command=self.view_dreams,
                  bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                  pady=8).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Delete Dream", command=self.delete_dream,
                  bg="#F44336", fg="white", font=("Arial", 10, "bold"),
                  pady=8).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Delete All Dreams", command=self.delete_all_dreams,
                  bg="#D32F2F", fg="white", font=("Arial", 10, "bold"),
                  pady=8).pack(fill=tk.X, pady=2)

        # ===== RIGHT SIDE - RESULTS AND VISUALIZATION =====
        # Create notebook (tabs) for different views
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Text Analysis
        analysis_tab = tk.Frame(self.notebook)
        self.notebook.add(analysis_tab, text="📊 Analysis Report")

        tk.Label(analysis_tab, text="Analysis Results",
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 10), padx=10)

        results_container = tk.Frame(analysis_tab, relief=tk.SUNKEN, borderwidth=1)
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.output_text = tk.Text(results_container, wrap=tk.WORD,
                                   font=("Arial", 10), state=tk.DISABLED,
                                   bg="#f5f5f5")
        output_scrollbar = tk.Scrollbar(results_container, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=output_scrollbar.set)

        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial message
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert("1.0", "Welcome to Dream Journal Analyzer! 🌙\n\n"
                                       "Add your dreams and click 'Analyze Dreams' to see insights.\n\n"
                                       "Your analysis results will appear here...\n\n"
                                       f"{'=' * 60}\n\n"
                                       "MOOD SCORE LEGEND:\n"
                                       "  😊 Very Positive:  +0.5 to +1.0\n"
                                       "  🙂 Positive:       +0.1 to +0.5\n"
                                       "  😐 Neutral:        -0.1 to +0.1\n"
                                       "  😔 Negative:       -0.5 to -0.1\n"
                                       "  😢 Very Negative:  -1.0 to -0.5\n\n"
                                       f"{'=' * 60}")
        self.output_text.config(state=tk.DISABLED)

        # Tab 2, 3, 4: Visualizations (only if matplotlib available)
        if VISUALIZER_AVAILABLE:
            # Timeline tab
            self.timeline_tab = tk.Frame(self.notebook)
            self.notebook.add(self.timeline_tab, text="📈 Mood Timeline")

            # Distribution tab
            self.distribution_tab = tk.Frame(self.notebook)
            self.notebook.add(self.distribution_tab, text="📊 Mood Distribution")

            # Themes tab
            self.themes_tab = tk.Frame(self.notebook)
            self.notebook.add(self.themes_tab, text="🔤 Top Themes")

            # Setup visualization tabs
            self._setup_visualization_tabs()
        else:
            # Show message about matplotlib
            no_viz_tab = tk.Frame(self.notebook)
            self.notebook.add(no_viz_tab, text="📈 Visualizations")

            msg = tk.Label(no_viz_tab,
                           text="📊 Visualizations Not Available\n\n"
                                "To enable interactive charts and graphs:\n\n"
                                "1. Install matplotlib:\n"
                                "   pip install matplotlib\n\n"
                                "2. Restart the application\n\n"
                                "All other features work perfectly without it!",
                           font=("Arial", 11),
                           justify=tk.LEFT,
                           fg="#666")
            msg.pack(expand=True, pady=50)

    def _setup_visualization_tabs(self):
        """Setup the visualization tabs with refresh buttons."""
        # Timeline tab
        timeline_controls = tk.Frame(self.timeline_tab)
        timeline_controls.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(timeline_controls, text="🔄 Refresh Timeline",
                  command=self.refresh_timeline,
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=5).pack(side=tk.LEFT)
        self.timeline_canvas_frame = tk.Frame(self.timeline_tab)
        self.timeline_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Distribution tab
        dist_controls = tk.Frame(self.distribution_tab)
        dist_controls.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(dist_controls, text="🔄 Refresh Distribution",
                  command=self.refresh_distribution,
                  bg="#673AB7", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=5).pack(side=tk.LEFT)
        self.dist_canvas_frame = tk.Frame(self.distribution_tab)
        self.dist_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Themes tab
        themes_controls = tk.Frame(self.themes_tab)
        themes_controls.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(themes_controls, text="🔄 Refresh Themes",
                  command=self.refresh_themes,
                  bg="#3F51B5", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=5).pack(side=tk.LEFT)
        self.themes_canvas_frame = tk.Frame(self.themes_tab)
        self.themes_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Show initial "click refresh" message
        for frame in [self.timeline_canvas_frame, self.dist_canvas_frame, self.themes_canvas_frame]:
            label = tk.Label(frame, text="Click 'Refresh' button above to generate visualization",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)

    def validate_date(self, date_str):
        """Validates date format and returns date object or None."""
        try:
            dream_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if dream_date > date.today():
                messagebox.showwarning("Invalid Date", "Dream date cannot be in the future.")
                return None
            return dream_date
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return None

    def add_dream(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        date_str = self.date_entry.get().strip()

        if not text:
            messagebox.showwarning("Empty Input", "Please enter your dream.")
            return

        dream_date = self.validate_date(date_str)
        if not dream_date:
            return

        dream = Dream(text, str(dream_date))
        self.journal.add_dream(dream)
        messagebox.showinfo("Success", "Dream saved successfully!")

        # Clear entry and reset date
        self.text_entry.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, str(date.today()))

    def show_analysis(self):
        analyzer = DreamAnalyzer(self.journal)
        result = analyzer.analyze()

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        if isinstance(result, str):
            self.output_text.insert("1.0", result)
        else:
            mood_interpretation = self.interpret_mood(result['average_mood'])
            text = (
                f"📊 DREAM ANALYSIS\n"
                f"{'=' * 60}\n\n"
                f"MOOD SCORE LEGEND:\n"
                f"  😊 Very Positive:  +0.5 to +1.0\n"
                f"  🙂 Positive:       +0.1 to +0.5\n"
                f"  😐 Neutral:        -0.1 to +0.1\n"
                f"  😔 Negative:       -0.5 to -0.1\n"
                f"  😢 Very Negative:  -1.0 to -0.5\n\n"
                f"{'=' * 60}\n\n"
                f"Total Dreams Recorded: {result['total_dreams']}\n\n"
                f"Average Mood Score: {result['average_mood']} {mood_interpretation}\n\n"
            )

            # Add individual dream mood scores
            text += f"Individual Dream Mood Scores:\n"
            for i, dream in enumerate(self.journal.dreams, 1):
                mood_str = f"{dream.mood_score:.3f}" if dream.mood_score is not None else "N/A"
                mood_interp = self.interpret_mood(dream.mood_score) if dream.mood_score is not None else ""
                preview = dream.text[:40] + "..." if len(dream.text) > 40 else dream.text
                text += f"  {i}. [{dream.date}] {mood_str} {mood_interp}\n"
                text += f"     \"{preview}\"\n"

            text += f"\nTop Recurring Themes:\n"
            for i, theme in enumerate(result['top_themes'], 1):
                text += f"  {i}. {theme.capitalize()}\n"

            text += f"\n{'=' * 60}\n"
            if VISUALIZER_AVAILABLE:
                text += "\n💡 TIP: Check out the visualization tabs above for interactive charts!\n"

            self.output_text.insert("1.0", text)

        self.output_text.config(state=tk.DISABLED)

    def interpret_mood(self, score):
        """Provides interpretation of mood score."""
        if score is None:
            return ""
        if score >= 0.5:
            return "😊 (Very Positive)"
        elif score >= 0.1:
            return "🙂 (Positive)"
        elif score >= -0.1:
            return "😐 (Neutral)"
        elif score >= -0.5:
            return "😔 (Negative)"
        else:
            return "😢 (Very Negative)"

    def refresh_timeline(self):
        """Refresh the mood timeline chart using visualizer.py."""
        if not VISUALIZER_AVAILABLE or not self.visualizer:
            return

        # Clear previous canvas
        for widget in self.timeline_canvas_frame.winfo_children():
            widget.destroy()

        if not self.journal.dreams:
            label = tk.Label(self.timeline_canvas_frame,
                             text="No dreams to visualize. Add some dreams first!",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)
            return

        # Use visualizer to create chart
        chart_widget = self.visualizer.create_mood_timeline(self.timeline_canvas_frame)

        if chart_widget:
            chart_widget.pack(fill=tk.BOTH, expand=True)
        else:
            label = tk.Label(self.timeline_canvas_frame,
                             text="No mood scores available. Click 'Analyze Dreams' first!",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)

    def refresh_distribution(self):
        """Refresh the mood distribution chart using visualizer.py."""
        if not VISUALIZER_AVAILABLE or not self.visualizer:
            return

        # Clear previous canvas
        for widget in self.dist_canvas_frame.winfo_children():
            widget.destroy()

        if not self.journal.dreams:
            label = tk.Label(self.dist_canvas_frame,
                             text="No dreams to visualize. Add some dreams first!",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)
            return

        # Use visualizer to create chart
        chart_widget = self.visualizer.create_mood_distribution(self.dist_canvas_frame)

        if chart_widget:
            chart_widget.pack(fill=tk.BOTH, expand=True)
        else:
            label = tk.Label(self.dist_canvas_frame,
                             text="No mood scores available. Click 'Analyze Dreams' first!",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)

    def refresh_themes(self):
        """Refresh the top themes chart using visualizer.py."""
        if not VISUALIZER_AVAILABLE or not self.visualizer:
            return

        # Clear previous canvas
        for widget in self.themes_canvas_frame.winfo_children():
            widget.destroy()

        if not self.journal.dreams:
            label = tk.Label(self.themes_canvas_frame,
                             text="No dreams to visualize. Add some dreams first!",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)
            return

        # Use visualizer to create chart
        chart_widget = self.visualizer.create_themes_chart(self.themes_canvas_frame)

        if chart_widget:
            chart_widget.pack(fill=tk.BOTH, expand=True)
        else:
            label = tk.Label(self.themes_canvas_frame,
                             text="No themes to visualize.",
                             font=("Arial", 11), fg="#666")
            label.pack(expand=True)

    def view_dreams(self):
        """Display all recorded dreams."""
        if not self.journal.dreams:
            messagebox.showinfo("No Dreams", "No dreams recorded yet.")
            return

        # Create new window
        dreams_window = tk.Toplevel(self.root)
        dreams_window.title("All Dreams")
        dreams_window.geometry("700x500")

        # Create frame with scrollbar
        frame = tk.Frame(dreams_window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="📖 Your Dream Journal",
                 font=("Arial", 14, "bold")).pack(pady=(0, 10))

        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Display dreams
        for i, dream in enumerate(reversed(self.journal.dreams), 1):
            mood_str = f" [Mood: {dream.mood_score:.2f}]" if dream.mood_score is not None else ""
            text_widget.insert(tk.END, f"\n{'=' * 60}\n")
            text_widget.insert(tk.END, f"Dream #{len(self.journal.dreams) - i + 1} - {dream.date}{mood_str}\n")
            text_widget.insert(tk.END, f"{'=' * 60}\n")
            text_widget.insert(tk.END, f"{dream.text}\n")

        text_widget.config(state=tk.DISABLED)

    def delete_dream(self):
        """Delete a specific dream by number."""
        if not self.journal.dreams:
            messagebox.showinfo("No Dreams", "No dreams to delete.")
            return

        # Create dialog window
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Dream")
        delete_window.geometry("500x400")
        delete_window.resizable(False, False)

        frame = tk.Frame(delete_window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Select a dream to delete:",
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))

        # Create listbox with scrollbar
        list_frame = tk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        dream_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                   font=("Arial", 9), selectmode=tk.SINGLE)
        dream_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=dream_listbox.yview)

        # Populate listbox
        for i, dream in enumerate(self.journal.dreams, 1):
            preview = dream.text[:50] + "..." if len(dream.text) > 50 else dream.text
            dream_listbox.insert(tk.END, f"{i}. [{dream.date}] {preview}")

        def confirm_delete():
            selection = dream_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a dream to delete.")
                return

            index = selection[0]
            dream = self.journal.dreams[index]
            preview = dream.text[:50] + "..." if len(dream.text) > 50 else dream.text

            if messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete this dream?\n\n"
                                   f"Date: {dream.date}\n"
                                   f"Preview: {preview}"):
                deleted = self.journal.delete_dream(index)
                if deleted:
                    messagebox.showinfo("Success", "Dream deleted successfully!")
                    delete_window.destroy()
                    # Refresh analysis if displayed
                    if self.output_text.get("1.0", tk.END).strip().startswith("📊"):
                        self.show_analysis()
                else:
                    messagebox.showerror("Error", "Failed to delete dream.")

        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Delete Selected", command=confirm_delete,
                  bg="#F44336", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=delete_window.destroy,
                  bg="#757575", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=5).pack(side=tk.LEFT, padx=5)

    def delete_all_dreams(self):
        """Delete all dreams after confirmation."""
        if not self.journal.dreams:
            messagebox.showinfo("No Dreams", "No dreams to delete.")
            return

        count = len(self.journal.dreams)
        response = messagebox.askyesnocancel(
            "⚠️ Delete All Dreams",
            f"Are you sure you want to delete ALL {count} dreams?\n\n"
            f"This action CANNOT be undone!\n\n"
            f"Click 'Yes' to confirm deletion."
        )

        if response:  # User clicked Yes
            self.journal.dreams.clear()
            self.journal.save_dreams()
            messagebox.showinfo("Success", f"All {count} dreams have been deleted.")

            # Clear analysis display
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "All dreams deleted. 🗑️\n\n"
                                           "Start recording new dreams to see analysis here.")
            self.output_text.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()