import string
from collections import Counter
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import nltk
import os

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Stop words list
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# Sentiment analysis function
def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    if score['compound'] > 0:
        return "Positive Sentiment"
    elif score['compound'] < 0:
        return "Negative Sentiment"
    else:
        return "Neutral Sentiment"

# Function to analyze emotions and sentiment
def analyze_text():
    text = input_text.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showwarning("Warning", "Please enter some text to analyze.")
        return

    # Text preprocessing
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = cleaned_text.split()
    
    # Removing stop words
    final_words = [word for word in tokenized_words if word not in stop_words]

    # NLP Emotion Algorithm
    emotion_list = []
    if os.path.exists('emotions.txt'):
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                if word in final_words:
                    emotion_list.append(emotion)

    # Count emotions
    emotion_counter = Counter(emotion_list)
    
    # Sentiment analysis
    sentiment = sentiment_analysis(cleaned_text)

    # Update GUI elements
    emotion_text.delete('1.0', tk.END)
    emotion_text.insert(tk.END, f"Emotion Count:\n{emotion_counter}\n")
    
    sentiment_label.config(text=f"Overall Sentiment: {sentiment}")

    # Plotting the emotions on the graph
    fig, ax = plt.subplots(facecolor='#f7f7f9')
    ax.bar(emotion_counter.keys(), emotion_counter.values(), color='#3498db')
    ax.set_title('Emotion Analysis', fontsize=14, color='#2c3e50')
    ax.set_facecolor('#ecf0f1')
    fig.autofmt_xdate()

    # Display the plot in the tkinter window
    for widget in plot_frame.winfo_children():
        widget.destroy()  # Clear previous plots
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def clear_text():
    # Clear input and output fields
    input_text.delete('1.0', tk.END)
    emotion_text.delete('1.0', tk.END)
    sentiment_label.config(text="Overall Sentiment: ")
    for widget in plot_frame.winfo_children():
        widget.destroy()

# GUI Setup
window = tk.Tk()
window.title("Emotion & Sentiment Analyzer")
window.geometry("900x600")
window.configure(bg='#f7f7f9')

# Frame for Title
title_frame = tk.Frame(window, bg='#2c3e50')
title_frame.pack(fill=tk.X)

title_label = tk.Label(title_frame, text="Emotion & Sentiment Analyzer", font=('Helvetica', 18, 'bold'), bg='#2c3e50', fg='white')
title_label.pack(pady=10)

# Main Frame to hold left and right sections
main_frame = tk.Frame(window, bg='#f7f7f9')
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame for Plot (Left Side)
plot_frame = tk.Frame(main_frame, bg='#f7f7f9')
plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Frame for Input and Analysis (Right Side)
input_frame = tk.Frame(main_frame, bg='#f7f7f9')
input_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

# Input label
input_label = tk.Label(input_frame, text="Enter your text below:", font=('Helvetica', 12), bg='#f7f7f9', fg='#34495e')
input_label.pack(anchor='w')

# Text widget to input text content
input_text = ScrolledText(input_frame, width=40, height=10, font=('Helvetica', 11))
input_text.pack(pady=10)

# Frame for Buttons
button_frame = tk.Frame(input_frame, bg='#f7f7f9')
button_frame.pack(pady=10)

# Buttons for Analyze and Clear
analyze_button = tk.Button(button_frame, text="Analyze Text", command=analyze_text, bg='#27ae60', fg='white', font=('Helvetica', 11, 'bold'), width=15)
analyze_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_text, bg='#e74c3c', fg='white', font=('Helvetica', 11, 'bold'), width=15)
clear_button.grid(row=0, column=1, padx=5)

# Text widget to display emotion counter
emotion_text = ScrolledText(input_frame, width=40, height=10, font=('Helvetica', 11))
emotion_text.pack(pady=10)

# Label to display overall sentiment
sentiment_label = tk.Label(input_frame, text="Overall Sentiment: ", font=('Helvetica', 14, 'bold'), bg='#f7f7f9', fg='#2c3e50')
sentiment_label.pack(pady=10)

# Run the GUI loop
window.mainloop()
