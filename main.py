# main.py
import tkinter as tk
from tkinter import messagebox
from ui_components import RoundedButton, GradientFrame
import questions
from utils import start_timer, generate_certificate
import random

# ------------------ APP SETUP ------------------
app = tk.Tk()
app.title("Python Quiz Game")
app.geometry("1000x700")
app.resizable(False, False)

# Global variables
user_name = ""
difficulty = ""
selected_questions = []
question_index = 0
score = 0
user_answers = []
time_left = 60
timer_running = False


# ------------------ CLEAR WINDOW ------------------
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


# ------------------ LOGIN PAGE ------------------
def build_login_page():
    clear_window()
    frame = GradientFrame(app, "#a29bfe", "#74b9ff")
    frame.pack(fill="both", expand=True)

    canvas = frame.canvas

    canvas.create_text(500, 100, text="🎓 Python Quiz Game", font=("Poppins", 36, "bold"), fill="#2d3436")
    canvas.create_text(500, 160, text="Welcome! Please enter your details below", font=("Poppins", 16),
                       fill="#2d3436")

    # --- Enter Name ---
    tk.Label(app, text="Enter Your Name:", font=("Poppins", 18), bg=frame.bg_color, fg="#2d3436").place(x=370, y=230)
    name_entry = tk.Entry(app, font=("Poppins", 18), width=25, justify="center", relief="solid", bd=1)
    name_entry.place(x=310, y=270)

    # --- Select Difficulty ---
    tk.Label(app, text="Select Difficulty Level:", font=("Poppins", 18), bg=frame.bg_color, fg="#2d3436").place(x=360, y=340)

    diff_var = tk.StringVar(value="easy")
    difficulties = ["easy", "medium", "hard"]

    for i, level in enumerate(difficulties):
        tk.Radiobutton(
            app,
            text=level.capitalize(),
            variable=diff_var,
            value=level,
            font=("Poppins", 16),
            bg=frame.bg_color,
            fg="#2d3436",
            activebackground=frame.bg_color,
            selectcolor="#81ecec"
        ).place(x=450, y=380 + (i * 40))

    # --- Start Button ---
    def start_quiz():
        global user_name, difficulty, selected_questions, score, user_answers
        user_name = name_entry.get().strip()
        difficulty = diff_var.get()
        score = 0
        user_answers = []

        if not user_name:
            messagebox.showwarning("Input Error", "Please enter your name!")
            return

        if difficulty == "easy":
            selected_questions = random.sample(questions.easy_questions, len(questions.easy_questions))
        elif difficulty == "medium":
            selected_questions = random.sample(questions.medium_questions, len(questions.medium_questions))
        else:
            selected_questions = random.sample(questions.hard_questions, len(questions.hard_questions))

        build_quiz_page()

    RoundedButton(app, "Start Quiz 🚀", command=start_quiz, color1="#74b9ff", color2="#81ecec").place(x=375, y=520)


# ------------------ QUIZ PAGE ------------------
def build_quiz_page():
    clear_window()
    global question_index, time_left
    question_index = 0
    time_left = 60
    load_question()


def load_question():
    clear_window()
    global question_index, time_left

    if question_index >= len(selected_questions):
        show_result_page()
        return

    q = selected_questions[question_index]

    frame = GradientFrame(app, "#74b9ff", "#a29bfe")
    frame.pack(fill="both", expand=True)
    canvas = frame.canvas

    canvas.create_text(500, 60, text=f"{difficulty.capitalize()} Level", font=("Poppins", 22, "bold"), fill="#2d3436")
    canvas.create_text(500, 100, text=f"Question {question_index + 1} of {len(selected_questions)}",
                       font=("Poppins", 18), fill="#2d3436")

    # Timer
    timer_label = tk.Label(app, text=f"⏳ Time Left: {time_left}s", font=("Poppins", 16, "bold"), fg="#e17055",
                           bg=frame.bg_color)
    timer_label.place(x=820, y=20)

    # Question
    tk.Label(app, text=q['question'], font=("Poppins", 20, "bold"), fg="#2d3436", bg=frame.bg_color,
             wraplength=800, justify="center").place(x=100, y=180)

    # Options
    def select_answer(i):
        global score
        user_answers.append(i)
        if i == q['answer']:
            score += 1
        next_question()

    for i, opt in enumerate(q['options']):
        RoundedButton(app, opt, command=lambda i=i: select_answer(i), color1="#a29bfe", color2="#81ecec").place(
            x=300, y=320 + (i * 70)
        )

    # Start countdown timer
    def next_due_to_timeout():
        user_answers.append(-1)
        next_question()

    start_timer(app, timer_label, time_left, next_due_to_timeout)


def next_question():
    global question_index
    question_index += 1
    load_question()


# ------------------ RESULT PAGE ------------------
def show_result_page():
    clear_window()
    frame = GradientFrame(app, "#81ecec", "#74b9ff")
    frame.pack(fill="both", expand=True)
    canvas = frame.canvas

    canvas.create_text(500, 120, text=f"🎉 Well Done, {user_name}!", font=("Poppins", 32, "bold"), fill="#2d3436")
    canvas.create_text(500, 180, text=f"Your Score: {score} / {len(selected_questions)}", font=("Poppins", 26, "bold"),
                       fill="#0984e3")

    def review_answers():
        show_review_page()

    def generate_cert():
        generate_certificate(user_name, score, len(selected_questions))

    RoundedButton(app, "Review Answers", command=review_answers, color1="#74b9ff", color2="#a29bfe").place(x=375, y=350)
    RoundedButton(app, "Get Certificate 🏆", command=generate_cert, color1="#55efc4", color2="#00b894").place(x=375, y=420)
    RoundedButton(app, "Exit", command=show_thankyou_page, color1="#fab1a0", color2="#ff7675").place(x=375, y=490)


# ------------------ REVIEW PAGE ------------------
def show_review_page():
    clear_window()
    frame = GradientFrame(app, "#a29bfe", "#81ecec")
    frame.pack(fill="both", expand=True)
    canvas = frame.canvas

    canvas.create_text(500, 80, text="📘 Review Your Answers", font=("Poppins", 32, "bold"), fill="#2d3436")

    container = tk.Frame(app, bg=frame.bg_color)
    container.place(x=80, y=130, width=850, height=450)

    canvas_scroll = tk.Canvas(container, bg=frame.bg_color, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas_scroll.yview)
    scroll_frame = tk.Frame(canvas_scroll, bg=frame.bg_color)

    scroll_frame.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
    canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i, q in enumerate(selected_questions):
        correct_idx = q['answer']
        user_idx = user_answers[i] if i < len(user_answers) else -1
        is_correct = (user_idx == correct_idx)

        color_bg = "#c8e6c9" if is_correct else "#ffeaa7"
        border_color = "#00b894" if is_correct else "#d63031"

        card = tk.Frame(scroll_frame, bg=color_bg, highlightbackground=border_color, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=10, fill="x", expand=True)

        tk.Label(card, text=f"Q{i+1}: {q['question']}", font=("Poppins", 16, "bold"), bg=color_bg, fg="#2d3436",
                 wraplength=800, justify="left").pack(anchor="w", pady=3)
        your_ans = q['options'][user_idx] if user_idx != -1 else "No Answer"
        tk.Label(card, text=f"Your Answer: {your_ans}", font=("Poppins", 14), bg=color_bg, fg="#2d3436").pack(anchor="w")
        tk.Label(card, text=f"Correct Answer: {q['options'][correct_idx]}", font=("Poppins", 14, "bold"),
                 bg=color_bg, fg="#0984e3").pack(anchor="w", pady=2)

    RoundedButton(app, "Exit Game ❌", command=show_thankyou_page, color1="#fab1a0", color2="#ff7675").place(x=375, y=600)


# ------------------ THANK YOU PAGE ------------------
def show_thankyou_page():
    clear_window()
    frame = GradientFrame(app, "#81ecec", "#a29bfe")
    frame.pack(fill="both", expand=True)
    canvas = frame.canvas

    canvas.create_text(500, 250, text=f"🎉 Thank You, {user_name}!", font=("Poppins", 32, "bold"), fill="#2d3436")
    canvas.create_text(500, 320, text="We hope you enjoyed playing the Python Quiz Game!", font=("Poppins", 18),
                       fill="#2d3436")
    RoundedButton(app, "Exit", command=app.destroy, color1="#fab1a0", color2="#ff7675").place(x=400, y=420)


# ------------------ START APP ------------------
build_login_page()
app.mainloop()
