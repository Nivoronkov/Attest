class ProfileAnalyzer:
    def __init__(self, name, belbin_roles, cattell_factors):
        self.name = name
        self.belbin_roles = belbin_roles        # Словарь, например: {'Генератор идей': 18, 'Мотиватор': 15...}
        self.cattell_factors = cattell_factors  # Словарь факторов (стены от 1 до 10): {'A': 8, 'B': 7, 'M': 9...}
        self.report = []

    def get_dominant_roles(self):
        # Сортируем роли Белбина по убыванию баллов и берем топ-2
        sorted_roles = sorted(self.belbin_roles.items(), key=lambda item: item[1], reverse=True)
        return [role[0] for role in sorted_roles[:2]]

    def analyze_intersections(self):
        dominant_roles = self.get_dominant_roles()
        self.report.append(f"Анализ профиля сотрудника: {self.name}\n")
        self.report.append(f"Доминирующие командные роли (Белбин): {', '.join(dominant_roles)}\n")
        self.report.append("-" * 40)

        # 1. Анализ роли "Генератор идей"
        if 'Генератор идей' in dominant_roles:
            self.report.append("\n[ОЦЕНКА РОЛИ: ГЕНЕРАТОР ИДЕЙ]")
            # Проверяем подтверждение по Кеттелу (Фактор M - Мечтательность/Практичность, B - Интеллект)
            if self.cattell_factors.get('M', 5) >= 7 and self.cattell_factors.get('B', 5) >= 7:
                self.report.append("ПОДТВЕРЖДЕНО: Высокий интеллект и развитое воображение по Кеттелу полностью подтверждают роль инноватора. Сотрудник способен решать нестандартные задачи.")
            elif self.cattell_factors.get('M', 5) <= 4:
                self.report.append("ПРОТИВОРЕЧИЕ: Сотрудник претендует на роль генератора идей, но тест Кеттела показывает высокую приземленность и практичность. Возможно, он путает генерацию идей с оптимизацией текущих процессов.")

        # 2. Анализ роли "Мотиватор"
        if 'Мотиватор' in dominant_roles:
            self.report.append("\n[ОЦЕНКА РОЛИ: МОТИВАТОР]")
            # Фактор E (Доминантность), Фактор H (Смелость)
            if self.cattell_factors.get('E', 5) >= 7 and self.cattell_factors.get('H', 5) >= 7:
                self.report.append("ПОДТВЕРЖДЕНО: Ярко выраженные лидерские качества, напористость и готовность брать ответственность.")
            elif self.cattell_factors.get('E', 5) <= 4:
                self.report.append("РИСК: Сотрудник стремится управлять командой, но по Кеттелу ему не хватает природной доминантности. Лидерство может даваться через сильный стресс.")

        # Здесь будут добавляться остальные проверки для всех 9 ролей...

        return "\n".join(self.report)

# --- Блок тестирования логики (запускается только если запустить этот файл напрямую) ---
if __name__ == "__main__":
    # Имитация данных, которые программа получит после прохождения тестов сотрудником
    mock_belbin = {'Генератор идей': 20, 'Мотиватор': 5, 'Педант': 12, 'Координатор': 8}
    mock_cattell = {'A': 5, 'B': 8, 'E': 3, 'H': 4, 'M': 8, 'Q3': 6} # Стены от 1 до 10
    
    analyzer = ProfileAnalyzer("Иван Иванов", mock_belbin, mock_cattell)
    print(analyzer.analyze_intersections())