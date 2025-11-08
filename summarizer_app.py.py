from transformers import pipeline
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load summarization model
summarizer = pipeline("summarization", model="google/flan-t5-small")

# Function to summarize text
def summarize_text(length_type):
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    # Clear previous output before summarizing
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "⏳ Generating summary... please wait...\n")
    root.update_idletasks()  

    if length_type == "short":
        max_len = 60
    elif length_type == "medium":
        max_len = 150
    else:
        max_len = 300

    try:
        # Force fresh summarization every time
        summary = summarizer(text, max_length=max_len, min_length=20, do_sample=False)
        output_text.delete("1.0", tk.END)  # clear "loading..." message
        output_text.insert(tk.END, summary[0]['summary_text'])
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"⚠️ Error: {e}")

# GUI Setup
root = tk.Tk()
root.title("AI Text Summarizer (Flan-T5)")
root.geometry("800x600")
root.config(bg="#f0f4f8")

title_label = tk.Label(root, text="AI Text Summarizer", font=("Arial", 18, "bold"), bg="#f0f4f8")
title_label.pack(pady=10)

# Input area
input_label = tk.Label(root, text="Enter your text below:", font=("Arial", 12), bg="#f0f4f8")
input_label.pack(anchor="w", padx=20)

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Arial", 11))
input_text.pack(padx=20, pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

short_btn = tk.Button(button_frame, text="Short Summary", width=15, bg="#6ca0dc", fg="white", command=lambda: summarize_text("short"))
short_btn.grid(row=0, column=0, padx=10)

medium_btn = tk.Button(button_frame, text="Medium Summary", width=15, bg="#4f86c6", fg="white", command=lambda: summarize_text("medium"))
medium_btn.grid(row=0, column=1, padx=10)

detailed_btn = tk.Button(button_frame, text="Detailed Summary", width=15, bg="#2f5d8a", fg="white", command=lambda: summarize_text("detailed"))
detailed_btn.grid(row=0, column=2, padx=10)

# Output area
output_label = tk.Label(root, text="Summary Output:", font=("Arial", 12), bg="#f0f4f8")
output_label.pack(anchor="w", padx=20)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Arial", 11), bg="#f9f9f9")
output_text.pack(padx=20, pady=10)

root.mainloop()
