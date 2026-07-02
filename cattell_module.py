# cattell_module.py

class CattellTest:
    def __init__(self):
        # 16 факторов личности
        self.factors = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4']
        
        # Ключи для подсчета сырых баллов
        # Формат: {номер_вопроса: {'factor': 'Название_фактора', 'a': балл, 'b': балл, 'c': балл}}
        # Для фактора B (вопросы 3, 4 и т.д.) вариант ответа 'b' (не знаю) обычно дает 0
        self.scoring_keys = {
            1:  {'factor': 'A', 'a': 2, 'b': 1, 'c': 0},
            2:  {'factor': 'A', 'a': 0, 'b': 1, 'c': 2},
            3:  {'factor': 'B', 'a': 0, 'b': 1, 'c': 0}, # Интеллект: правильный ответ 'b'
            4:  {'factor': 'B', 'a': 1, 'b': 0, 'c': 0}, # Интеллект: правильный ответ 'a'
            5:  {'factor': 'C', 'a': 2, 'b': 1, 'c': 0},
            # ... здесь прописываются остальные 100 вопросов ...
            105: {'factor': 'Q4', 'a': 0, 'b': 1, 'c': 2}
        }

        # Таблицы перевода сырых баллов в стены (Stens)
        # В идеале нужно две таблицы (для мужчин и женщин), здесь показана структура одной
        # Формат: {'Фактор': {сырой_балл: стен}}
        self.sten_tables_general = {
            'A': {
                0: 1, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 
                6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10 # Максимум 12 сырых баллов
            },
            'B': {
                0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 
                6: 8, 7: 9, 8: 10 # У фактора B максимум 8 баллов (в форме C)
            }
            # ... словари для остальных факторов ...
        }

    def calculate_raw_scores(self, user_answers):
        """
        user_answers: словарь вида {номер_вопроса: 'выбранная_буква' (a, b или c)}
        """
        raw_scores = {factor: 0 for factor in self.factors}
        
        for q_num, answer in user_answers.items():
            # Если сотрудник случайно пропустил вопрос или ответил некорректно, пропускаем
            if q_num not in self.scoring_keys or answer not in ['a', 'b', 'c']:
                continue
                
            key_data = self.scoring_keys[q_num]
            factor = key_data['factor']
            points = key_data[answer]
            
            raw_scores[factor] += points
            
        return raw_scores

    def convert_to_stens(self, raw_scores):
        """Переводит сырые баллы в 10-балльную шкалу"""
        stens = {}
        for factor, raw_score in raw_scores.items():
            # Если фактор описан в таблице перевода
            if factor in self.sten_tables_general:
                table = self.sten_tables_general[factor]
                # Безопасное получение стена. Если сырой балл вышел за пределы таблицы (ошибка ввода), 
                # берем ближайшее крайнее значение
                if raw_score in table:
                    stens[factor] = table[raw_score]
                elif raw_score < min(table.keys()):
                    stens[factor] = 1
                else:
                    stens[factor] = 10
            else:
                # Если таблицы пока нет (для тестирования)
                stens[factor] = None 
                
        return stens

# --- Блок тестирования модуля ---
if __name__ == "__main__":
    test_cattell = CattellTest()
    
    # Имитация ответов сотрудника
    mock_answers = {
        1: 'a',  # Фактор A: +2 балла
        2: 'b',  # Фактор A: +1 балл (итого A = 3)
        3: 'b',  # Фактор B: +1 балл
        4: 'a',  # Фактор B: +1 балл (итого B = 2)
        5: 'c'   # Фактор C: +0 баллов
    }
    
    print("1. Подсчет сырых баллов:")
    raw = test_cattell.calculate_raw_scores(mock_answers)
    print(raw) # Увидим A: 3, B: 2, остальные по 0
    
    print("\n2. Перевод в стены (шкала 1-10):")
    final_stens = test_cattell.convert_to_stens(raw)
    print(f"Фактор A: {final_stens['A']} стенов")
    print(f"Фактор B: {final_stens['B']} стенов")