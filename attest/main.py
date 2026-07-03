# -*- coding: utf-8 -*-
"""
main.py
Программа аттестации персонала: объединённое тестирование по двум методикам.

  1. 16-факторный личностный опросник Р. Кеттелла, форма C (105 вопросов);
  2. Опросник командных ролей Р. М. Белбина (7 блоков по 8 утверждений).

После прохождения обоих тестов программа подсчитывает результаты, строит
объединённый профиль (analyzer.py), показывает отчёт на экране и сохраняет
его в документ Word (report_module.py).

Запуск:  python main.py
Зависимости:  pip install python-docx  (для сохранения отчёта в Word)
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from cattell_module import CattellTest
from belbin_module import BelbinTest
from analyzer import ProfileAnalyzer
import report_module


class AssessmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аттестация персонала: профиль сотрудника")
        self.root.geometry("780x640")
        self.root.minsize(680, 560)

        # Подключаем модули методик
        self.cattell_test = CattellTest()
        self.belbin_test = BelbinTest()

        # Данные сотрудника
        self.employee_name = tk.StringVar()
        self.employee_dept = tk.StringVar()

        # Хранилища ответов
        self.cattell_answers = {}
        self.belbin_answers = {}

        self.show_welcome_screen()

    # ==================================================================
    # СЛУЖЕБНОЕ
    # ==================================================================
    def clear_window(self):
        """Удаляет все элементы с экрана для отрисовки новых."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================================================================
    # ЭКРАНЫ ПРИВЕТСТВИЯ И РЕГИСТРАЦИИ
    # ==================================================================
    def show_welcome_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Добро пожаловать в систему аттестации",
                 font=("Arial", 18, "bold")).pack(pady=40)

        tk.Label(self.root,
                 text="Вам предстоит пройти два психологических опросника:\n\n"
                      "1. Опросник Кеттелла (105 вопросов) — личностный профиль;\n"
                      "2. Опросник Белбина (7 блоков) — командные роли.\n\n"
                      "По результатам будет сформирован единый отчёт.\n"
                      "Время прохождения: примерно 30-40 минут.\n\n"
                      "Отвечайте искренне: в опроснике нет «правильных» и «неправильных»\n"
                      "ответов, а достоверность контролируется специальной шкалой.",
                 font=("Arial", 12), justify="center").pack(pady=20)

        tk.Button(self.root, text="Начать тестирование", font=("Arial", 14),
                  command=self.show_registration_screen, width=22, height=2).pack(pady=30)

    def show_registration_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Регистрация участника",
                 font=("Arial", 18, "bold")).pack(pady=40)

        tk.Label(self.root, text="Введите ваше ФИО:", font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.root, textvariable=self.employee_name,
                 font=("Arial", 12), width=40).pack(pady=5)

        tk.Label(self.root, text="Укажите вашу должность и отдел:",
                 font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.root, textvariable=self.employee_dept,
                 font=("Arial", 12), width=40).pack(pady=5)

        tk.Button(self.root, text="Перейти к первому тесту", font=("Arial", 14),
                  command=self.validate_registration, width=25, height=2).pack(pady=40)

    def validate_registration(self):
        """Проверка, что сотрудник ввёл данные перед стартом."""
        if len(self.employee_name.get().strip()) < 3 or len(self.employee_dept.get().strip()) < 2:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")
        else:
            self.start_cattell_test()

    # ==================================================================
    # БЛОК ТЕСТА КЕТТЕЛЛА
    # ==================================================================
    def start_cattell_test(self):
        self.cattell_answers = {}
        self.current_q_num = 1
        self.total_questions = len(self.cattell_test.questions)
        self.show_cattell_question()

    def show_cattell_question(self):
        self.clear_window()

        # Если вопросы закончились — переходим к Белбину
        if self.current_q_num > self.total_questions:
            self.start_belbin_test()
            return

        q_text, ans_a, ans_b, ans_c = self.cattell_test.questions[self.current_q_num]

        # Индикатор прогресса
        tk.Label(self.root,
                 text=f"Тест 1 из 2: опросник Кеттелла — вопрос {self.current_q_num} из {self.total_questions}",
                 font=("Arial", 10, "italic"), fg="gray").pack(pady=8)

        progress = tk.Canvas(self.root, width=560, height=8,
                             bg="#e0e0e0", highlightthickness=0)
        progress.pack()
        progress.create_rectangle(
            0, 0, 560 * self.current_q_num / self.total_questions, 8,
            fill="#4a90d9", width=0)

        tk.Label(self.root, text=f"{self.current_q_num}. {q_text}",
                 font=("Arial", 14), wraplength=640, justify="center").pack(pady=28)

        for letter, text in (('a', ans_a), ('b', ans_b), ('c', ans_c)):
            tk.Button(self.root, text=text, font=("Arial", 12),
                      width=52, wraplength=520,
                      command=lambda l=letter: self.save_cattell_answer_and_next(l)
                      ).pack(pady=5)

        # Кнопка возврата к предыдущему вопросу
        if self.current_q_num > 1:
            tk.Button(self.root, text="← Вернуться к предыдущему вопросу",
                      font=("Arial", 10), fg="gray",
                      command=self.previous_cattell_question).pack(pady=18)

    def save_cattell_answer_and_next(self, answer_key):
        """Сохраняет ответ и переключает на следующий вопрос."""
        self.cattell_answers[self.current_q_num] = answer_key
        self.current_q_num += 1
        self.show_cattell_question()

    def previous_cattell_question(self):
        if self.current_q_num > 1:
            self.current_q_num -= 1
            self.show_cattell_question()

    # ==================================================================
    # БЛОК ТЕСТА БЕЛБИНА
    # ==================================================================
    def start_belbin_test(self):
        self.clear_window()
        tk.Label(self.root, text="Тест Кеттелла завершён!",
                 font=("Arial", 16, "bold"), fg="#00722e").pack(pady=40)
        tk.Label(self.root,
                 text="Сейчас начнётся тест командных ролей Белбина.\n\n"
                      "В каждом из 7 блоков вам нужно распределить ровно 10 баллов\n"
                      "между 8 утверждениями: чем точнее утверждение описывает вас,\n"
                      "тем больше баллов ему отдайте. Можно отдать все 10 баллов\n"
                      "одному утверждению или распределить их между несколькими.",
                 font=("Arial", 12), justify="center").pack(pady=20)

        tk.Button(self.root, text="Начать тест Белбина", font=("Arial", 14), width=25,
                  command=self.init_belbin_data).pack(pady=40)

    def init_belbin_data(self):
        self.belbin_answers = {}
        self.current_belbin_block = 1
        self.total_blocks = len(self.belbin_test.questions)
        self.show_belbin_block()

    def show_belbin_block(self):
        self.clear_window()

        # Если блоки закончились — считаем результаты
        if self.current_belbin_block > self.total_blocks:
            self.finish_assessment()
            return

        block_data = self.belbin_test.questions[self.current_belbin_block]

        tk.Label(self.root,
                 text=f"Тест 2 из 2: опросник Белбина — блок {self.current_belbin_block} из {self.total_blocks}",
                 font=("Arial", 10, "italic"), fg="gray").pack(pady=5)
        tk.Label(self.root, text=block_data["title"],
                 font=("Arial", 12, "bold"), wraplength=680).pack(pady=8)

        # Индикатор суммы баллов (обновляется при каждом изменении)
        self.sum_label = tk.Label(self.root, text="Распределено баллов: 0 из 10",
                                  font=("Arial", 11, "bold"), fg="#c00000")
        self.sum_label.pack(pady=4)

        frame = tk.Frame(self.root)
        frame.pack(pady=4, fill="both", expand=True, padx=20)

        self.point_vars = []
        for item_text in block_data["items"]:
            row_frame = tk.Frame(frame)
            row_frame.pack(fill="x", pady=2)

            var = tk.IntVar(value=0)
            var.trace_add("write", lambda *args: self.update_belbin_sum())
            self.point_vars.append(var)

            tk.Spinbox(row_frame, from_=0, to=10, textvariable=var, width=3,
                       font=("Arial", 11), state="readonly").pack(side="right", padx=8)
            tk.Label(row_frame, text=item_text, font=("Arial", 10),
                     wraplength=580, justify="left", anchor="w").pack(side="left", fill="x", expand=True)

        btn_text = ("Завершить тестирование"
                    if self.current_belbin_block == self.total_blocks
                    else "Следующий блок")
        tk.Button(self.root, text=btn_text, font=("Arial", 12),
                  command=self.validate_and_save_belbin).pack(pady=12)

    def update_belbin_sum(self):
        total = sum(var.get() for var in self.point_vars)
        color = "#00722e" if total == 10 else "#c00000"
        self.sum_label.config(text=f"Распределено баллов: {total} из 10", fg=color)

    def validate_and_save_belbin(self):
        """Проверяет сумму баллов в блоке и сохраняет ответы."""
        current_points = [var.get() for var in self.point_vars]

        if not self.belbin_test.validate_block_points(current_points):
            messagebox.showwarning(
                "Ошибка ввода",
                f"Сумма баллов в блоке должна быть ровно 10.\n"
                f"Сейчас вы распределили: {sum(current_points)}")
            return

        self.belbin_answers[self.current_belbin_block] = current_points
        self.current_belbin_block += 1
        self.show_belbin_block()

    # ==================================================================
    # ФИНАЛ: ПОДСЧЁТ, ОБЪЕДИНЁННЫЙ ОТЧЁТ, СОХРАНЕНИЕ
    # ==================================================================
    def finish_assessment(self):
        name = self.employee_name.get().strip()
        dept = self.employee_dept.get().strip()

        # 1. Обсчёт Кеттелла: сырые баллы -> стены -> проверка достоверности
        cattell_results = self.cattell_test.get_full_results(self.cattell_answers)

        # 2. Обсчёт Белбина: баллы по 8 командным ролям
        belbin_results = self.belbin_test.calculate_results(self.belbin_answers)

        # 3. Объединённый анализ двух методик
        analyzer = ProfileAnalyzer(name, dept, belbin_results, cattell_results,
                                   belbin_test=self.belbin_test,
                                   cattell_test=self.cattell_test)
        report_text = analyzer.analyze_intersections()

        # 4. Сохранение отчёта в Word (или txt, если python-docx не установлен)
        try:
            report_path, warn = report_module.save_report(
                name, dept, cattell_results, belbin_results,
                analyzer, self.cattell_test, self.belbin_test)
        except Exception as e:
            report_path, warn = None, f"Не удалось сохранить отчёт: {e}"

        # 5. Вывод на экран
        self.show_report_screen(report_text, report_path, warn)

    def show_report_screen(self, report_text, report_path, warn):
        self.clear_window()

        tk.Label(self.root, text="Тестирование успешно завершено!",
                 font=("Arial", 16, "bold"), fg="#00722e").pack(pady=10)

        if report_path:
            tk.Label(self.root, text=f"Отчёт сохранён в файл:\n{report_path}",
                     font=("Arial", 10), fg="#333333").pack(pady=2)
        if warn:
            tk.Label(self.root, text=warn, font=("Arial", 10),
                     fg="#c00000", justify="center").pack(pady=2)

        text_widget = ScrolledText(self.root, font=("Courier New", 10),
                                   wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True, padx=15, pady=10)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Пройти тест заново", font=("Arial", 12),
                  command=self.show_welcome_screen).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Закрыть программу", font=("Arial", 12),
                  command=self.root.destroy).pack(side="left", padx=10)


# ==========================================
# ТОЧКА ВХОДА В ПРОГРАММУ
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AssessmentApp(root)
    root.mainloop()
