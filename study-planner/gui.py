# gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from ai_module import generate_reviewer  # Placeholder for AI reviewer generation
import data_manager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study Planner")
        self.geometry("1000x700")
        self.configure(bg="#f7f6f3")

        data_manager.init_db()
        self.selected_subject_id = None
        self.selected_topic_id = None
        self.active_tab = "notes"

        self.create_layout()
        self.refresh_subjects()

    def create_layout(self):
        # Sidebar for subjects
        self.sidebar = tk.Frame(self, bg="#ececec", width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Subjects", bg="#ececec", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))

        self.subjects_frame = tk.Frame(self.sidebar, bg="#ececec")
        self.subjects_frame.pack(fill="y", expand=True)

        self.add_subject_entry = tk.Entry(self.sidebar, font=("Segoe UI", 12))
        self.add_subject_entry.pack(padx=10, pady=(10, 0), fill="x")
        self.add_subject_entry.bind("<Return>", lambda e: self.add_subject())

        self.add_subject_btn = tk.Button(self.sidebar, text="Add Subject", command=self.add_subject, bg="#d1e7dd", font=("Segoe UI", 11))
        self.add_subject_btn.pack(padx=10, pady=(5, 20), fill="x")

        # Main content area
        self.content = tk.Frame(self, bg="#f7f6f3")
        self.content.pack(side="left", fill="both", expand=True)

        self.subject_title = tk.Label(self.content, text="Select a subject", bg="#f7f6f3", font=("Segoe UI", 18, "bold"))
        self.subject_title.pack(pady=(30, 10))

        self.topics_frame = tk.Frame(self.content, bg="#f7f6f3")
        self.topics_frame.pack(fill="x", padx=40)

        self.add_topic_entry = tk.Entry(self.content, font=("Segoe UI", 12))
        self.add_topic_entry.pack(padx=40, pady=(10, 0), fill="x")
        self.add_topic_entry.bind("<Return>", lambda e: self.add_topic())

        self.add_topic_btn = tk.Button(self.content, text="Add Topic", command=self.add_topic, bg="#e2eafc", font=("Segoe UI", 11))
        self.add_topic_btn.pack(padx=40, pady=(5, 20), fill="x")

        self.topic_title = tk.Label(self.content, text="", bg="#f7f6f3", font=("Segoe UI", 15, "bold"))
        self.topic_title.pack(pady=(10, 0))

        # --- Tab Buttons ---
        self.tab_frame = tk.Frame(self.content, bg="#f7f6f3")
        self.tab_frame.pack(padx=40, pady=(10, 0), anchor="w")

        self.notes_tab_btn = tk.Button(self.tab_frame, text="Notes", command=self.show_notes_tab, bg="#b6e0fe", font=("Segoe UI", 11))
        self.notes_tab_btn.pack(side="left", padx=2)
        self.reviewer_tab_btn = tk.Button(self.tab_frame, text="Reviewer", command=self.show_reviewer_tab, bg="#f7f6f3", font=("Segoe UI", 11))
        self.reviewer_tab_btn.pack(side="left", padx=2)
        self.quiz_tab_btn = tk.Button(self.tab_frame, text="Quiz", command=self.show_quiz_tab, bg="#f7f6f3", font=("Segoe UI", 11))
        self.quiz_tab_btn.pack(side="left", padx=2)

        # --- Notes Widget ---
        self.notes_text = scrolledtext.ScrolledText(self.content, width=90, height=15, font=("Segoe UI", 12), wrap="word")
        self.notes_text.pack(padx=40, pady=(10, 0), fill="both", expand=False)
        self.notes_text.bind("<KeyRelease>", lambda e: self.save_notes())

        # --- Reviewer Widgets ---
        self.reviewer_btn = tk.Button(self.content, text="Generate Reviewer (AI)", command=self.generate_reviewer, bg="#ffe066", font=("Segoe UI", 11))
        self.reviewer_text = scrolledtext.ScrolledText(self.content, width=90, height=15, font=("Segoe UI", 12), wrap="word")
        self.reviewer_text.bind("<KeyRelease>", lambda e: self.save_reviewer())
        self.progress = ttk.Progressbar(self.content, mode='indeterminate')

        # --- Quiz Widgets (placeholder, not implemented yet) ---
        self.quiz_label = tk.Label(self.content, text="Quiz feature coming soon!", bg="#f7f6f3", font=("Segoe UI", 13))

        self.show_notes_tab()

    # --- Tab Switching Methods ---
    def show_notes_tab(self):
        self.active_tab = "notes"
        self.notes_tab_btn.config(bg="#b6e0fe")
        self.reviewer_tab_btn.config(bg="#f7f6f3")
        self.quiz_tab_btn.config(bg="#f7f6f3")
        self.notes_text.pack(padx=40, pady=(10, 0), fill="both", expand=False)
        self.reviewer_btn.pack_forget()
        self.reviewer_text.pack_forget()  # <-- changed from reviewer_label
        self.progress.pack_forget()
        self.quiz_label.pack_forget()

    def show_reviewer_tab(self):
        self.active_tab = "reviewer"
        self.notes_tab_btn.config(bg="#f7f6f3")
        self.reviewer_tab_btn.config(bg="#ffe066")
        self.quiz_tab_btn.config(bg="#f7f6f3")
        self.notes_text.pack_forget()
        self.quiz_label.pack_forget()
        self.reviewer_btn.pack(padx=40, pady=(10, 0), fill="x")
        self.reviewer_text.pack(padx=40, pady=(10, 0), fill="both", expand=True)  # <-- changed from reviewer_label
        self.progress.pack_forget()
        self.load_reviewer()  # Ensure reviewer is loaded when switching tabs

    def show_quiz_tab(self):
        self.active_tab = "quiz"
        self.notes_tab_btn.config(bg="#f7f6f3")
        self.reviewer_tab_btn.config(bg="#f7f6f3")
        self.quiz_tab_btn.config(bg="#ffe066")
        self.notes_text.pack_forget()
        self.reviewer_btn.pack_forget()
        self.reviewer_text.pack(padx=40, pady=(10, 0), fill="both", expand=True)  # <-- changed from reviewer_label
        self.progress.pack_forget()
        self.quiz_label.pack(padx=40, pady=(10, 0), fill="both", expand=True)

    def refresh_topics(self):
        for widget in self.topics_frame.winfo_children():
            widget.destroy()
        if self.selected_subject_id is None:
            return
        topics = data_manager.get_topics(self.selected_subject_id)
        for tid, name, *_ in topics:
            btn = tk.Button(self.topics_frame, text=name, anchor="w", bg="#f7f6f3", font=("Segoe UI", 12),
                            relief="flat", command=lambda tid=tid, name=name: self.select_topic(tid, name))
            btn.pack(side="left", padx=5, pady=5)

    def select_subject(self, subject_id, subject_name):
        self.selected_subject_id = subject_id
        self.selected_topic_id = None
        self.subject_title.config(text=subject_name)
        self.topic_title.config(text="")
        self.notes_text.delete("1.0", tk.END)
        self.reviewer_text.delete("1.0", tk.END)
        self.refresh_topics()  # <-- This must be called to update the topics list

    def add_subject(self):
        name = self.add_subject_entry.get().strip()
        if name:
            data_manager.add_subject(name)
            self.add_subject_entry.delete(0, tk.END)
            self.refresh_subjects()

    def refresh_topics(self):
        for widget in self.topics_frame.winfo_children():
            widget.destroy()
        if self.selected_subject_id is None:
            return
        topics = data_manager.get_topics(self.selected_subject_id)
        for tid, name, _ in topics:
            btn = tk.Button(self.topics_frame, text=name, anchor="w", bg="#f7f6f3", font=("Segoe UI", 12),
                            relief="flat", command=lambda tid=tid, name=name: self.select_topic(tid, name))
            btn.pack(side="left", padx=5, pady=5)

    def add_topic(self):
        name = self.add_topic_entry.get().strip()
        if name and self.selected_subject_id is not None:
            data_manager.add_topic(self.selected_subject_id, name)
            self.add_topic_entry.delete(0, tk.END)
            self.refresh_topics()
            self.show_notes_tab()  # <-- Add this line to update the UI

    def select_topic(self, topic_id, topic_name):
        self.selected_topic_id = topic_id
        self.topic_title.config(text=topic_name)
        notes = ""
        topics = data_manager.get_topics(self.selected_subject_id)
        for tid, name, n in topics:
            if tid == topic_id:
                notes = n or ""
                break
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(tk.END, notes)
        self.reviewer_text.delete("1.0", tk.END)
        self.load_reviewer()

    def save_notes(self):
        if self.selected_topic_id is not None:
            notes = self.notes_text.get("1.0", tk.END).strip()
            data_manager.update_topic_notes(self.selected_topic_id, notes)

    def generate_reviewer(self):
        if self.selected_subject_id is None or self.selected_topic_id is None:
            self.reviewer_text.delete("1.0", tk.END)
            self.reviewer_text.insert(tk.END, "Please select a subject and topic first.")
            return

        subject_name = self.subject_title.cget("text")
        topic_name = self.topic_title.cget("text")
        notes = self.notes_text.get("1.0", tk.END).strip()

        self.reviewer_text.delete("1.0", tk.END)
        self.reviewer_text.insert(tk.END, "Generating reviewer...")
        self.progress.pack(padx=40, pady=(5, 0), fill="x")
        self.progress.start()

        def ai_task():
            try:
                reviewer = generate_reviewer(subject_name, topic_name, notes)
                data_manager.save_reviewer(self.selected_topic_id, reviewer)
            except Exception as e:
                reviewer = f"Error generating reviewer: {e}"
            self.reviewer_text.after(0, lambda: self.display_reviewer(reviewer))

        threading.Thread(target=ai_task, daemon=True).start()

    def display_reviewer(self, reviewer):
        self.progress.stop()
        self.progress.pack_forget()
        self.reviewer_text.delete("1.0", tk.END)
        self.reviewer_text.insert(tk.END, reviewer)

    def load_reviewer(self):
        if self.selected_topic_id is not None:
            reviewer = data_manager.get_reviewer(self.selected_topic_id)
            self.reviewer_text.delete("1.0", tk.END)
            if reviewer:
                self.reviewer_text.insert(tk.END, reviewer)
            else:
                self.reviewer_text.insert(tk.END, "No reviewer generated yet.")

    def save_reviewer(self):
        if self.selected_topic_id is not None:
            reviewer = self.reviewer_text.get("1.0", tk.END).strip()
            data_manager.save_reviewer(self.selected_topic_id, reviewer)