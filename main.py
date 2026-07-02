import tkinter as tk
from tkinter import messagebox

class AssessmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аттестация персонала: Профиль сотрудника")
        # Компактный размер для удобной работы в мультиоконном режиме
        self.root.geometry("600x400")
        
        # Переменные для хранения данных сотрудника
        self.employee_name = tk.StringVar()
        self.employee_dept = tk.StringVar()
        
        # Запускаем первый экран
        self.show_welcome_screen()

    def clear_window(self):
        """Удаляет все элементы с экрана для отрисовки новых"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # ЭКРАНЫ ПРИВЕТСТВИЯ И РЕГИСТРАЦИИ
    # ==========================================

    def show_welcome_screen(self):
        self.clear_window()
        
        title = tk.Label(self.root, text="Добро пожаловать в систему аттестации", font=("Arial", 18, "bold"))
        title.pack(pady=40)
        
        desc = tk.Label(self.root, text="Вам предстоит пройти два психологических опросника.\nЭто поможет нам лучше понять ваши сильные стороны и командные роли.\nВремя прохождения: ~30-40 минут.", 
                        font=("Arial", 12), justify="center")
        desc.pack(pady=20)
        
        start_btn = tk.Button(self.root, text="Начать тестирование", font=("Arial", 14), 
                              command=self.show_registration_screen, width=20, height=2)
        start_btn.pack(pady=30)

    def show_registration_screen(self):
        self.clear_window()
        
        title = tk.Label(self.root, text="Регистрация участника", font=("Arial", 18, "bold"))
        title.pack(pady=40)
        
        # Поле ввода ФИО
        tk.Label(self.root, text="Введите ваше ФИО:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(self.root, textvariable=self.employee_name, font=("Arial", 12), width=40)
        name_entry.pack(pady=5)
        
        # Поле ввода Отдела
        tk.Label(self.root, text="Укажите вашу должность и отдел:", font=("Arial", 12)).pack(pady=5)
        dept_entry = tk.Entry(self.root, textvariable=self.employee_dept, font=("Arial", 12), width=40)
        dept_entry.pack(pady=5)
        
        next_btn = tk.Button(self.root, text="Перейти к первому тесту", font=("Arial", 14), 
                             command=self.validate_registration, width=25, height=2)
        next_btn.pack(pady=40)

    def validate_registration(self):
        """Проверка, что сотрудник ввел данные перед стартом"""
        if len(self.employee_name.get().strip()) < 3 or len(self.employee_dept.get().strip()) < 2:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")
        else:
            self.start_cattell_test()

    # ==========================================
    # БЛОК ТЕСТА КЕТТЕЛА
    # ==========================================

    def start_cattell_test(self):
        # Словарь для хранения ответов сотрудника {номер_вопроса: 'a', 'b' или 'c'}
        self.cattell_answers = {}
        self.current_q_num = 1
        
        # Заглушка из 3 вопросов (в реальности здесь будут все 105)
        self.cattell_questions_text = {
            1: ("1. Я хорошо понял инструкцию к этому тесту.", "Да", "Не уверен", "Нет"),
            2: ("2. Я готов(а) отвечать на вопросы максимально искренне.", "Да", "Не уверен", "Нет"),
            3: ("3. Выберите логическое продолжение: Дом относится к комнате так же, как дерево к...", "Лесу", "Растению", "Листу")
        }
        
        self.show_cattell_question()

    def show_cattell_question(self):
        self.clear_window()
        
        # Если вопросы закончились, переходим к Белбину
        if self.current_q_num > len(self.cattell_questions_text):
            self.start_belbin_test()
            return

        # Достаем текст вопроса и варианты ответов
        q_data = self.cattell_questions_text[self.current_q_num]
        q_text = q_data[0]
        ans_a_text = q_data[1]
        ans_b_text = q_data[2]
        ans_c_text = q_data[3]

        # Индикатор прогресса
        progress = tk.Label(self.root, text=f"Вопрос {self.current_q_num} из {len(self.cattell_questions_text)}", font=("Arial", 10, "italic"), fg="gray")
        progress.pack(pady=10)

        # Текст вопроса
        lbl_question = tk.Label(self.root, text=q_text, font=("Arial", 14), wraplength=550, justify="center")
        lbl_question.pack(pady=30)

        # Кнопки ответов (привязываем к ним метод сохранения ответа)
        btn_a = tk.Button(self.root, text=ans_a_text, font=("Arial", 12), width=30, 
                          command=lambda: self.save_cattell_answer_and_next('a'))
        btn_a.pack(pady=5)

        btn_b = tk.Button(self.root, text=ans_b_text, font=("Arial", 12), width=30, 
                          command=lambda: self.save_cattell_answer_and_next('b'))
        btn_b.pack(pady=5)

        btn_c = tk.Button(self.root, text=ans_c_text, font=("Arial", 12), width=30, 
                          command=lambda: self.save_cattell_answer_and_next('c'))
        btn_c.pack(pady=5)

    def save_cattell_answer_and_next(self, answer_key):
        """Сохраняет ответ и переключает на следующий вопрос"""
        self.cattell_answers[self.current_q_num] = answer_key
        self.current_q_num += 1
        self.show_cattell_question()

    # ==========================================
    # ПЕРЕХОД К ТЕСТУ БЕЛБИНА
    # ==========================================

# ==========================================
    # БЛОК ТЕСТА БЕЛБИНА
    # ==========================================

    def start_belbin_test(self):
        self.clear_window()
        tk.Label(self.root, text="Тест Кеттела завершен!", font=("Arial", 16, "bold")).pack(pady=40)
        tk.Label(self.root, text="Сейчас начнется тест командных ролей.\nВам нужно будет распределить ровно 10 баллов\nмежду 8 утверждениями в каждой из 7 ситуаций.", font=("Arial", 12), justify="center").pack(pady=20)
        
        tk.Button(self.root, text="Начать тест Белбина", font=("Arial", 14), width=25, 
                  command=self.init_belbin_data).pack(pady=40)

    def init_belbin_data(self):
        self.belbin_answers = {}
        self.current_belbin_block = 1
        
        # Данные для блоков Белбина (добавлены 2 блока для примера)
        self.belbin_blocks_text = {
            1: {
                "title": "Блок 1: Что, как я думаю, я могу привнести в команду:",
                "items": [
                    "А. Я быстро замечаю и использую новые возможности.",
                    "Б. Я могу хорошо работать с самыми разными людьми.",
                    "В. Генерация идей — мое естественное качество.",
                    "Г. Моя сила в способности выявлять ценность в чужих мыслях.",
                    "Д. Моя главная черта — доводить дела до конца.",
                    "Е. Я готов временно стать непопулярным ради результата.",
                    "Ж. Я быстро чувствую, что сработает в знакомой ситуации.",
                    "З. Я могу предложить обоснованную альтернативу без предвзятости."
                ]
            },
            2: {
                "title": "Блок 2: Если у меня есть недостатки в командной работе, то они в том, что:",
                "items": [
                    "А. Я чувствую себя неуютно, пока собрание четко не структурировано.",
                    "Б. Я склонен соглашаться с теми, чья точка зрения не получила поддержки.",
                    "В. Я много говорю, когда команда переходит к новым идеям.",
                    "Г. Мой кругозор заставляет меня скептически относиться к поспешным выводам.",
                    "Д. Меня иногда считают слишком резким, если нужно сдвинуть дело с места.",
                    "Е. Мне трудно вести за собой, я предпочитаю быть внутри процесса.",
                    "Ж. Я могу увлечься идеей и потерять нить происходящего.",
                    "З. Мои коллеги считают, что я излишне беспокоюсь о деталях."
                ]
            }
            # Сюда позже добавите блоки 3-7
        }
        self.show_belbin_block()

    def show_belbin_block(self):
        self.clear_window()
        
        # Если блоки закончились, переходим к финалу
        if self.current_belbin_block > len(self.belbin_blocks_text):
            self.finish_assessment()
            return
            
        block_data = self.belbin_blocks_text[self.current_belbin_block]
        
        tk.Label(self.root, text=f"Блок {self.current_belbin_block} из {len(self.belbin_blocks_text)}", font=("Arial", 10, "italic"), fg="gray").pack(pady=5)
        tk.Label(self.root, text=block_data["title"], font=("Arial", 12, "bold"), wraplength=550).pack(pady=10)
        tk.Label(self.root, text="Распределите ровно 10 баллов:", font=("Arial", 10), fg="blue").pack(pady=5)

        # Фрейм для списка утверждений
        frame = tk.Frame(self.root)
        frame.pack(pady=5, fill="x", padx=20)
        
        # Список переменных, которые будут хранить цифры из виджетов Spinbox
        self.point_vars = []
        
        for i, item_text in enumerate(block_data["items"]):
            row_frame = tk.Frame(frame)
            row_frame.pack(fill="x", pady=2)
            
            tk.Label(row_frame, text=item_text, font=("Arial", 10), wraplength=450, justify="left").pack(side="left")
            
            # Переменная для конкретного поля (по умолчанию 0)
            var = tk.IntVar(value=0)
            self.point_vars.append(var)
            
            # Поле со стрелочками (от 0 до 10)
            spinbox = tk.Spinbox(row_frame, from_=0, to=10, textvariable=var, width=3, font=("Arial", 10), state="readonly")
            spinbox.pack(side="right", padx=10)

        tk.Button(self.root, text="Следующий блок", font=("Arial", 12), command=self.validate_and_save_belbin).pack(pady=15)

    def validate_and_save_belbin(self):
        """Проверяет сумму баллов и сохраняет ответы"""
        # Достаем текущие значения из всех 8 полей
        current_points = [var.get() for var in self.point_vars]
        total_points = sum(current_points)
        
        if total_points != 10:
            # Выбрасываем системное предупреждение, если сумма не равна 10
            messagebox.showwarning("Ошибка ввода", f"Сумма баллов должна быть ровно 10.\nСейчас вы распределили: {total_points}")
            return
            
        # Если всё верно, записываем в словарь и идем дальше
        self.belbin_answers[self.current_belbin_block] = current_points
        self.current_belbin_block += 1
        self.show_belbin_block()

    # ==========================================
    # ФИНАЛ И СОХРАНЕНИЕ
    # ==========================================

    def finish_assessment(self):
        self.clear_window()
        tk.Label(self.root, text="Тестирование успешно завершено!", font=("Arial", 16, "bold"), fg="green").pack(pady=50)
        
        # Здесь мы выводим собранные словари на экран для проверки, 
        # на следующем этапе мы передадим их в наши математические модули.
        summary_text = f"Сотрудник: {self.employee_name.get()} ({self.employee_dept.get()})\n\n"
        summary_text += f"Ответы Кеттел: {self.cattell_answers}\n"
        summary_text += f"Ответы Белбин: {self.belbin_answers}"
        
        tk.Label(self.root, text=summary_text, font=("Arial", 10), wraplength=550, justify="left").pack(pady=20)
        tk.Button(self.root, text="Закрыть программу", font=("Arial", 12), command=self.root.destroy).pack(pady=30)

# ==========================================
# ТОЧКА ВХОДА В ПРОГРАММУ
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AssessmentApp(root)
    root.mainloop()