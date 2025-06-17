import customtkinter as ctk
import random
import time
import threading
import pygame
import tkinter as tk

pygame.mixer.init()

quotes = [
    "This too shall pass.",
    "Take a deep breath. You are doing fine.",
    "You are stronger than your anxiety.",
    "Inhale calm, exhale stress.",
    "One moment at a time."
]

slime_faces = ["(≧▽≦)", "(♥‿♥)", "(•ω•)", "(≧◡≦)", "(◕‿◕)"]
slime_reactions = [
    "Squish! 😄",
    "So soft~ 🫧",
    "Wiggle wiggle! 💚",
    "Again! 😆",
    "Squish therapy complete 💆"
]

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# === Splash Screen ===
splash = ctk.CTk()
splash.geometry("600x400")
splash.title("Loading Delta Labs")
splash.resizable(False, False)

logo_label = ctk.CTkLabel(splash, text="Δ", font=("Arial", 100, "bold"))
logo_label.pack(pady=10)

title_label = ctk.CTkLabel(splash, text="Delta Labs", font=("Arial", 32))
title_label.pack(pady=5)

loading_label = ctk.CTkLabel(splash, text="Loading...", font=("Arial", 16))
loading_label.pack(pady=20)

progress = ctk.CTkProgressBar(splash, mode="indeterminate")
progress.pack(pady=10, padx=100)
progress.start()

def start_app():
    splash.destroy()

    # === Main App ===
    app = ctk.CTk()
    app.title("Anxiety Relief App")
    app.geometry("1000x650")
    app.resizable(False, False)

    # === Tabbed Interface ===
    tabs = ctk.CTkTabview(app)
    tabs.pack(expand=True, fill="both", padx=20, pady=20)

    # === Tabs ===
    tabs.add("Home")
    tabs.add("Quotes")
    tabs.add("Breathing")
    tabs.add("Journal")
    tabs.add("Music")
    tabs.add("Slime Game")

    # === Home Tab ===
    home_tab = tabs.tab("Home")
    home_title = ctk.CTkLabel(home_tab, text="Welcome to the Anxiety Relief App", font=("Arial", 26))
    home_title.pack(pady=20)

    home_desc = ctk.CTkLabel(home_tab, text="Hey, this is AkAritraS from Delta-Labs. This app helps you to cure stress, anxiety and pain. Don't worry, everything will be fine! Just have faith in yourself!",
                              wraplength=800, justify="center", font=("Arial", 16))
    home_desc.pack(pady=10)

    nav_frame = ctk.CTkFrame(home_tab)
    nav_frame.pack(pady=20)

    ctk.CTkButton(nav_frame, text="Go to Quotes", command=lambda: tabs.set("Quotes")).grid(row=0, column=0, padx=10, pady=10)
    ctk.CTkButton(nav_frame, text="Breathing Exercise", command=lambda: tabs.set("Breathing")).grid(row=0, column=1, padx=10, pady=10)
    ctk.CTkButton(nav_frame, text="Journal", command=lambda: tabs.set("Journal")).grid(row=0, column=2, padx=10, pady=10)
    ctk.CTkButton(nav_frame, text="Music Player", command=lambda: tabs.set("Music")).grid(row=0, column=3, padx=10, pady=10)
    ctk.CTkButton(nav_frame, text="Slime Game", command=lambda: tabs.set("Slime Game")).grid(row=0, column=4, padx=10, pady=10)

    # === Quotes Tab ===
    quote_tab = tabs.tab("Quotes")
    quote_label = ctk.CTkLabel(quote_tab, text=random.choice(quotes), font=("Arial", 20), wraplength=600, justify="center")
    quote_label.pack(pady=40)

    def new_quote():
        quote_label.configure(text=random.choice(quotes))

    ctk.CTkButton(quote_tab, text="New Quote", command=new_quote).pack()

    # === Breathing Tab ===
    breathing_tab = tabs.tab("Breathing")
    breath_label = ctk.CTkLabel(breathing_tab, text="", font=("Arial", 28))
    breath_label.pack(pady=20)

    circle = tk.Canvas(breathing_tab, width=200, height=200, bg="white", highlightthickness=0)
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

    ctk.CTkButton(breathing_tab, text="Start Breathing", command=breathing_exercise).pack(pady=10)

    # === Journal Tab ===
    journal_tab = tabs.tab("Journal")
    journal_label = ctk.CTkLabel(journal_tab, text="Gratitude Journal", font=("Arial", 20))
    journal_label.pack(pady=10)

    journal_entry = ctk.CTkTextbox(journal_tab, width=600, height=200)
    journal_entry.pack(pady=10)

    journal_status = ctk.CTkLabel(journal_tab, text="", font=("Arial", 12))
    journal_status.pack(pady=5)

    def save_journal():
        with open("gratitude_journal.txt", "a") as f:
            f.write(journal_entry.get("0.0", "end").strip() + "\n---\n")
        journal_entry.delete("0.0", "end")
        journal_status.configure(text="Saved!")
        app.after(2000, lambda: journal_status.configure(text=""))

    ctk.CTkButton(journal_tab, text="Save Journal", command=save_journal).pack(pady=5)

    # === Music Tab ===
    music_tab = tabs.tab("Music")

    def play_music():
        try:
            pygame.mixer.music.load("relaxing_music.mp3")
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading music:", e)

    def stop_music():
        pygame.mixer.music.stop()

    ctk.CTkButton(music_tab, text="Play Music", command=play_music).pack(pady=10)
    ctk.CTkButton(music_tab, text="Stop Music", command=stop_music).pack(pady=10)

    # === Slime Game Tab ===
    slime_tab = tabs.tab("Slime Game")
    slime_title = ctk.CTkLabel(slime_tab, text="Squishy Slime!", font=("Arial", 22))
    slime_title.pack(pady=10)

    canvas = tk.Canvas(slime_tab, width=300, height=300, bg="#ffffff", highlightthickness=0)
    canvas.pack(pady=10)

    slime = canvas.create_oval(50, 50, 250, 250, fill="#77dd77", outline="#55cc55", width=2)
    face = canvas.create_text(150, 150, text=random.choice(slime_faces), font=("Arial", 26))
    slime_msg = ctk.CTkLabel(slime_tab, text="", font=("Arial", 16))
    slime_msg.pack(pady=10)

    def animate_squish():
        squish_frames = [
            (70, 80, 230, 220),
            (85, 105, 215, 195),
            (95, 110, 205, 190),
            (85, 105, 215, 195),
            (70, 80, 230, 220),
            (50, 50, 250, 250)
        ]
        for shape in squish_frames:
            canvas.coords(slime, *shape)
            canvas.itemconfig(face, text=random.choice(slime_faces))
            slime_msg.configure(text=random.choice(slime_reactions))
            canvas.update()
            time.sleep(0.08)
        canvas.coords(slime, 50, 50, 250, 250)
        canvas.itemconfig(face, text="(◕‿◕)")

    canvas.tag_bind(slime, "<Button-1>", lambda e: threading.Thread(target=animate_squish).start())
    canvas.tag_bind(face, "<Button-1>", lambda e: threading.Thread(target=animate_squish).start())

    # === Theme Switch (Top Right) ===
    def change_theme(mode):
        ctk.set_appearance_mode(mode)

    settings_frame = ctk.CTkFrame(app, fg_color="transparent")
    settings_frame.place(relx=0.98, rely=0.01, anchor="ne")
    ctk.CTkLabel(settings_frame, text="Theme:").pack(side="left")
    theme_switch = ctk.CTkOptionMenu(settings_frame, values=["Light", "Dark", "System"], command=change_theme)
    theme_switch.set("Light")
    theme_switch.pack(side="left", padx=5)

    app.mainloop()

splash.after(5000, start_app)
splash.mainloop()
