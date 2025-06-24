import customtkinter as ctk
import tkinter as tk
import threading
import time
import random
import pygame
from datetime import datetime

pygame.mixer.init()

# === Setup ===
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

quotes = [
    "This too shall pass.",
    "Take a deep breath. You are doing fine.",
    "You are stronger than your anxiety.",
    "Inhale calm, exhale stress.",
    "One moment at a time."
]

tips = [
    "Start your day with gratitude 🙏",
    "Take a walk for 10 minutes 🍃",
    "Drink some water 💧",
    "Smile at yourself in the mirror 😊",
    "Listen to calming music 🎶"
]

slime_faces = ["(≧▽≦)", "(♥‿♥)", "(•ω•)", "(≧◡≦)", "(◕‿◕)"]
slime_reactions = ["Squish! 😄", "So soft~ 🫧", "Wiggle wiggle! 💚", "Again! 😆", "Squish therapy complete 💆"]

# === Splash Screen ===
splash = ctk.CTk()
splash.geometry("600x400")
splash.title("Loading Delta Labs")
splash.resizable(False, False)

logo_label = ctk.CTkLabel(splash, text="Δ", font=("Arial", 100, "bold"))
logo_label.pack(pady=10)

title_label = ctk.CTkLabel(splash, text="Delta Labs", font=("Arial", 32))
title_label.pack(pady=5)

loading_label = ctk.CTkLabel(splash, text="Loading Anxiety Relief App...", font=("Arial", 16))
loading_label.pack(pady=20)

progress = ctk.CTkProgressBar(splash, mode="indeterminate")
progress.pack(pady=10, padx=100)
progress.start()

# === Function to Start Main App ===
def start_app():
    splash.destroy()

    app = ctk.CTk()
    app.title("Anxiety Relief App")
    app.geometry("1100x700")
    app.resizable(False, False)

    # === Sidebar ===
    sidebar = ctk.CTkFrame(app, width=180)
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text="Δ Delta Labs", font=("Arial", 24, "bold")).pack(pady=20)

    pages = {}
    def show_page(name):
        for page in pages.values():
            page.pack_forget()
        pages[name].pack(expand=True, fill="both")

    buttons = [
        ("Home", lambda: show_page("home")),
        ("Quotes", lambda: show_page("quotes")),
        ("Breathing", lambda: show_page("breathing")),
        ("Journal", lambda: show_page("journal")),
        ("Music", lambda: show_page("music")),
        ("Slime Game", lambda: show_page("slime")),
        ("Anxiety Info", lambda: show_page("info")),
    ]

    for text, command in buttons:
        ctk.CTkButton(sidebar, text=text, command=command).pack(pady=8, padx=10, fill="x")

    # Theme switcher
    def change_theme(mode): ctk.set_appearance_mode(mode)
    ctk.CTkLabel(sidebar, text="Theme:").pack(pady=(20, 5))
    ctk.CTkOptionMenu(sidebar, values=["Light", "Dark", "System"], command=change_theme).pack(padx=10)

    # === Main Content Area ===
    content = ctk.CTkFrame(app)
    content.pack(side="left", expand=True, fill="both")

    # === Pages ===
    home = ctk.CTkFrame(content)
    pages["home"] = home
    ctk.CTkLabel(home, text="Welcome to the Anxiety Relief App", font=("Arial", 26)).pack(pady=20)
    ctk.CTkLabel(home, text="This app helps you reduce stress, anxiety, and emotional tension.\nStay strong. You’ve got this!",
                 font=("Arial", 16), wraplength=800, justify="center").pack(pady=10)
    today_tip = random.choice(tips)
    ctk.CTkLabel(home, text=f"🌟 Daily Tip: {today_tip}", font=("Arial", 18, "italic")).pack(pady=30)

    # Quotes Page
    quotes_page = ctk.CTkFrame(content)
    pages["quotes"] = quotes_page
    quote_label = ctk.CTkLabel(quotes_page, text=random.choice(quotes), font=("Arial", 20), wraplength=600)
    quote_label.pack(pady=40)
    ctk.CTkButton(quotes_page, text="New Quote", command=lambda: quote_label.configure(text=random.choice(quotes))).pack()

    # Breathing Page
    breathing = ctk.CTkFrame(content)
    pages["breathing"] = breathing
    breath_label = ctk.CTkLabel(breathing, text="", font=("Arial", 28))
    breath_label.pack(pady=20)
    circle = tk.Canvas(breathing, width=200, height=200, bg="white", highlightthickness=0)
    circle.pack()
    circle_obj = circle.create_oval(50, 50, 150, 150, fill="#aee2ff")

    def breathing_exercise():
        def animate():
            for _ in range(3):
                breath_label.configure(text="Inhale... 🫁")
                for i in range(10):
                    circle.coords(circle_obj, 50 - i*2, 50 - i*2, 150 + i*2, 150 + i*2)
                    time.sleep(0.05)
                breath_label.configure(text="Hold... ✋")
                time.sleep(2)
                breath_label.configure(text="Exhale... 💨")
                for i in range(10):
                    circle.coords(circle_obj, 30 + i*2, 30 + i*2, 170 - i*2, 170 - i*2)
                    time.sleep(0.05)
            breath_label.configure(text="Done. Feel better? 😊")
        threading.Thread(target=animate).start()

    ctk.CTkButton(breathing, text="Start Breathing", command=breathing_exercise).pack(pady=10)

    # Journal Page
    journal = ctk.CTkFrame(content)
    pages["journal"] = journal
    ctk.CTkLabel(journal, text="Gratitude Journal", font=("Arial", 20)).pack(pady=10)
    journal_entry = ctk.CTkTextbox(journal, width=600, height=200)
    journal_entry.pack(pady=10)
    journal_status = ctk.CTkLabel(journal, text="", font=("Arial", 12))
    journal_status.pack()

    def save_journal():
        with open("gratitude_journal.txt", "a") as f:
            f.write(journal_entry.get("0.0", "end").strip() + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n---\n")
        journal_entry.delete("0.0", "end")
        journal_status.configure(text="Saved!")
        app.after(2000, lambda: journal_status.configure(text=""))

    ctk.CTkButton(journal, text="Save Journal", command=save_journal).pack(pady=5)

    # Music Page
    music = ctk.CTkFrame(content)
    pages["music"] = music

    def play_music():
        try:
            pygame.mixer.music.load("relaxing_music.mp3")
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Music error:", e)

    ctk.CTkLabel(music, text="Relaxing Music", font=("Arial", 20)).pack(pady=10)
    ctk.CTkButton(music, text="Play Music", command=play_music).pack(pady=5)
    ctk.CTkButton(music, text="Stop Music", command=lambda: pygame.mixer.music.stop()).pack(pady=5)

    # Slime Game
    slime = ctk.CTkFrame(content)
    pages["slime"] = slime
    ctk.CTkLabel(slime, text="Squishy Slime!", font=("Arial", 22)).pack(pady=10)
    canvas = tk.Canvas(slime, width=300, height=300, bg="#ffffff", highlightthickness=0)
    canvas.pack(pady=10)
    slime_obj = canvas.create_oval(50, 50, 250, 250, fill="#77dd77", outline="#55cc55", width=2)
    slime_face = canvas.create_text(150, 150, text=random.choice(slime_faces), font=("Arial", 26))
    slime_msg = ctk.CTkLabel(slime, text="", font=("Arial", 16))
    slime_msg.pack(pady=10)

    def animate_squish():
        frames = [(70, 80, 230, 220), (85, 105, 215, 195), (95, 110, 205, 190),
                  (85, 105, 215, 195), (70, 80, 230, 220), (50, 50, 250, 250)]
        for shape in frames:
            canvas.coords(slime_obj, *shape)
            canvas.itemconfig(slime_face, text=random.choice(slime_faces))
            slime_msg.configure(text=random.choice(slime_reactions))
            canvas.update()
            time.sleep(0.08)

    canvas.tag_bind(slime_obj, "<Button-1>", lambda e: threading.Thread(target=animate_squish).start())
    canvas.tag_bind(slime_face, "<Button-1>", lambda e: threading.Thread(target=animate_squish).start())

    # Anxiety Info
    info = ctk.CTkFrame(content)
    pages["info"] = info
    ctk.CTkLabel(info, text="Understanding Anxiety", font=("Arial", 22)).pack(pady=10)
    info_text = ctk.CTkTextbox(info, width=900, height=500, wrap="word", font=("Arial", 14))
    info_text.pack(pady=10)
    info_content = """
📘 What is Anxiety?
Anxiety is a natural response to stress. It becomes a disorder when it’s excessive and affects daily life.

🔍 Common Causes:
• Chronic stress
• Traumatic events
• Poor sleep, diet
• Hormonal imbalances

🛠️ Solutions:
✓ Deep breathing
✓ Exercise
✓ Therapy or support
✓ Balanced lifestyle

❌ Avoid:
✗ Isolation
✗ Overthinking
✗ Substance use
✗ Avoiding problems

🌟 You're not alone. It gets better.
"""
    info_text.insert("0.0", info_content)
    info_text.configure(state="disabled")

    # Show home by default
    show_page("home")
    app.mainloop()

# === After splash screen delay, launch app ===
splash.after(3000, start_app)
splash.mainloop()
