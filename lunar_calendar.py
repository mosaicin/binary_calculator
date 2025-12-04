
import math
import hashlib
from datetime import datetime, timedelta
import json

class LunarCalendar:
    def __init__(self):
        # Лунный цикл: 29.530588 дней
        self.lunar_month = 29.530588
        self.lunar_days = [
            (1, "Новолуние", "Начало нового цикла", "Загадывание желаний"),
            (2, "Растущий серп", "Энергия роста", "Планирование"),
            (3, "Растущий серп", "Накопление сил", "Обучение"),
            (4, "Растущий серп", "Принятие решений", "Выбор пути"),
            (5, "Растущий серп", "Активность", "Действие"),
            (6, "Растущий серп", "Вдохновение", "Творчество"),
            (7, "Первая четверть", "Баланс", "Анализ"),
            (8, "Растущая Луна", "Уверенность", "Достижения"),
            (9, "Растущая Луна", "Интуиция", "Озарения"),
            (10, "Растущая Луна", "Социальность", "Общение"),
            (11, "Растущая Луна", "Практичность", "Работа"),
            (12, "Растущая Луна", "Эмоции", "Чувства"),
            (13, "Растущая Луна", "Глубина", "Тайны"),
            (14, "Растущая Луна", "Изобилие", "Избыток"),
            (15, "Полнолуние", "Пик энергии", "Осознание"),
            (16, "Убывающая Луна", "Отпускание", "Прощение"),
            (17, "Убывающая Луна", "Смирение", "Принятие"),
            (18, "Убывающая Луна", "Очищение", "Избавление"),
            (19, "Убывающая Луна", "Анализ", "Пересмотр"),
            (20, "Убывающая Луна", "Фокус", "Концентрация"),
            (21, "Третья четверть", "Кризис", "Перелом"),
            (22, "Убывающая Луна", "Трансформация", "Изменение"),
            (23, "Убывающая Луна", "Сила", "Выносливость"),
            (24, "Убывающая Луна", "Порядок", "Структура"),
            (25, "Убывающая Луна", "Скорость", "Импульс"),
            (26, "Убывающая Луна", "Мудрость", "Опыт"),
            (27, "Убывающая Луна", "Отдых", "Восстановление"),
            (28, "Убывающий серп", "Подведение итогов", "Завершение"),
            (29, "Тёмная Луна", "Пустота", "Отпускание"),
            (30, "Тёмная Луна", "Безмолвие", "Подготовка")
        ]
        
        # Лунные знаки (созвездия лунного зодиака)
        self.lunar_signs = [
            ("Овен", "🔥", "Действие, инициатива", 0, 30),
            ("Телец", "🌿", "Стабильность, ресурсы", 30, 60),
            ("Близнецы", "💭", "Общение, информация", 60, 90),
            ("Рак", "🌊", "Эмоции, дом", 90, 120),
            ("Лев", "👑", "Творчество, самовыражение", 120, 150),
            ("Дева", "📊", "Анализ, работа", 150, 180),
            ("Весы", "⚖️", "Гармония, отношения", 180, 210),
            ("Скорпион", "🦂", "Трансформация, тайны", 210, 240),
            ("Стрелец", "🏹", "Расширение, философия", 240, 270),
            ("Козерог", "⛰️", "Цели, структура", 270, 300),
            ("Водолей", "💡", "Инновации, свобода", 300, 330),
            ("Рыбы", "🐠", "Интуиция, духовность", 330, 360)
        ]
        
        # Известное новолуние для расчётов (6 января 2000 года)
        self.reference_new_moon = datetime(2000, 1, 6, 18, 14)
    
    def calculate_moon_phase(self, date=None):
        """Вычисляет фазу Луны для указанной даты"""
        if date is None:
            date = datetime.now()
        
        # Вычисляем разницу в днях от известного новолуния
        delta_days = (date - self.reference_new_moon).total_seconds() / 86400
        
        # Находим возраст Луны (дни от последнего новолуния)
        moon_age = delta_days % self.lunar_month
        
        # Вычисляем фазу в процентах (0% - новолуние, 100% - следующее новолуние)
        phase_percent = (moon_age / self.lunar_month) * 100
        
        # Определяем лунный день (1-30)
        lunar_day = int(moon_age) + 1
        if lunar_day > 30:
            lunar_day = 30
        
        # Определяем фазу по проценту
        if phase_percent < 1:
            phase_name = "🌑 Новолуние"
        elif phase_percent < 25:
            phase_name = "🌒 Растущий серп"
        elif phase_percent < 50:
            phase_name = "🌓 Первая четверть"
        elif phase_percent < 75:
            phase_name = "🌔 Растущая Луна"
        elif phase_percent < 99:
            phase_name = "🌕 Полнолуние"
        elif phase_percent < 101:
            phase_name = "🌖 Убывающая Луна"
        else:
            phase_name = "🌘 Убывающий серп"
        
        return {
            'date': date,
            'moon_age_days': moon_age,
            'phase_percent': phase_percent,
            'phase_name': phase_name,
            'lunar_day': lunar_day,
            'days_until_full': (self.lunar_month / 2 - moon_age) if moon_age < self.lunar_month/2 else 0,
            'days_until_new': self.lunar_month - moon_age
        }
    
    def get_lunar_day_info(self, lunar_day):
        """Возвращает информацию о лунном дне"""
        if 1 <= lunar_day <= 30:
            day_num, name, energy, advice = self.lunar_days[lunar_day-1]
            return {
                'day': day_num,
                'name': name,
                'energy': energy,
                'advice': advice,
                'symbol': self.get_lunar_day_symbol(lunar_day)
            }
        return None
    
    def get_lunar_day_symbol(self, lunar_day):
        """Возвращает символ для лунного дня"""
        symbols = [
            "🌑", "🌒", "🌒", "🌒", "🌒", "🌒", "🌓", 
            "🌔", "🌔", "🌔", "🌔", "🌔", "🌔", "🌔", 
            "🌕", "🌖", "🌖", "🌖", "🌖", "🌖", "🌗",
            "🌘", "🌘", "🌘", "🌘", "🌘", "🌘", "🌘",
            "🌑", "🌑"
        ]
        return symbols[lunar_day-1] if 1 <= lunar_day <= 30 else "🌙"
    
    def calculate_lunar_position(self, date=None):
        """Вычисляет положение Луны в знаке зодиака"""
        if date is None:
            date = datetime.now()
        
        # Упрощённый расчёт: Луна проходит 360° за 27.3 дня
        days_since_ref = (date - self.reference_new_moon).total_seconds() / 86400
        # Сидерический месяц (относительно звёзд): 27.321661 дня
        sidereal_month = 27.321661
        lunar_longitude = (days_since_ref % sidereal_month) / sidereal_month * 360
        
        # Находим лунный знак
        for sign, symbol, description, start, end in self.lunar_signs:
            if start <= lunar_longitude < end:
                return {
                    'sign': sign,
                    'symbol': symbol,
                    'description': description,
                    'longitude': lunar_longitude,
                    'degrees_in_sign': lunar_longitude - start
                }
        
        return {'sign': 'Овен', 'symbol': '🔥', 'longitude': 0}
    
    def word_to_lunar_influence(self, word, date=None):
        """Определяет влияние Луны на слово"""
        if date is None:
            date = datetime.now()
        
        # Вычисляем фазу Луны
        moon_phase = self.calculate_moon_phase(date)
        
        # Преобразуем слово в числовой код
        word_hash = hashlib.md5(word.encode()).hexdigest()
        word_number = int(word_hash[:8], 16)  # Берём первые 8 символов
        
        # Связываем слово с лунным днём
        lunar_day = moon_phase['lunar_day']
        lunar_day_info = self.get_lunar_day_info(lunar_day)
        
        # Определяем лунный знак
        lunar_position = self.calculate_lunar_position(date)
        
        # Вычисляем влияние на основе хеша
        influence_level = (word_number % 100) / 100  # 0.0 до 1.0
        
        # Определяем тип влияния
        if influence_level < 0.25:
            influence_type = "Слабое"
            effect = "Минимальное воздействие"
        elif influence_level < 0.5:
            influence_type = "Умеренное"
            effect = "Заметное влияние"
        elif influence_level < 0.75:
            influence_type = "Сильное"
            effect = "Значительное воздействие"
        else:
            influence_type = "Очень сильное"
            effect = "Мощное трансформирующее влияние"
        
        # Определяем рекомендации на основе фазы
        phase = moon_phase['phase_percent']
        if phase < 25:  # Растущая Луна
            recommendation = "Благоприятное время для начала дел, связанных со словом"
        elif phase < 50:  # Первая четверть
            recommendation = "Время активных действий и реализации"
        elif phase < 75:  # Полнолуние
            recommendation = "Пик влияния, время осознания и проявления"
        else:  # Убывающая Луна
            recommendation = "Время завершения, анализа и подготовки"
        
        return {
            'word': word,
            'date': date.strftime("%d.%m.%Y %H:%M"),
            'moon_phase': moon_phase['phase_name'],
            'lunar_day': lunar_day,
            'lunar_day_info': lunar_day_info,
            'lunar_sign': lunar_position['sign'],
            'lunar_symbol': lunar_position['symbol'],
            'influence_level': influence_level,
            'influence_type': influence_type,
            'effect': effect,
            'recommendation': recommendation,
            'word_hash': word_hash[:16] + "..."
        }
    
    def generate_lunar_calendar(self, start_date=None, days=30):
        """Генерирует лунный календарь на указанный период"""
        if start_date is None:
            start_date = datetime.now()
        
        calendar = []
        current_date = start_date
        
        for day in range(days):
            moon_info = self.calculate_moon_phase(current_date)
            lunar_pos = self.calculate_lunar_position(current_date)
            
            calendar.append({
                'date': current_date.strftime("%d.%m.%Y"),
                'day_of_week': current_date.strftime("%A"),
                'moon_phase': moon_info['phase_name'],
                'lunar_day': moon_info['lunar_day'],
                'lunar_sign': lunar_pos['sign'],
                'lunar_symbol': lunar_pos['symbol'],
                'phase_percent': round(moon_info['phase_percent'], 1)
            })
            
            current_date += timedelta(days=1)
        
        return calendar
    
    def find_best_date_for_word(self, word, start_date=None, period_days=60):
        """Находит лучшую дату для работы со словом"""
        if start_date is None:
            start_date = datetime.now()
        
        best_dates = []
        current_date = start_date
        
        # Преобразуем слово в числовой код для анализа
        word_hash = hashlib.md5(word.encode()).hexdigest()
        word_code = int(word_hash[:4], 16) % 100
        
        for day in range(period_days):
            moon_phase = self.calculate_moon_phase(current_date)
            lunar_day_info = self.get_lunar_day_info(moon_phase['lunar_day'])
            
            # Оцениваем благоприятность
            score = 0
            
            # Фаза Луны: растущая благоприятна для новых начинаний
            if moon_phase['phase_percent'] < 50:
                score += 30
            
            # Лунный день: некоторые дни более благоприятны
            favorable_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            if moon_phase['lunar_day'] in favorable_days:
                score += 20
            
            # Совместимость с кодом слова
            if (word_code % moon_phase['lunar_day']) < 10:
                score += 25
            
            # День недели
            weekday = current_date.strftime("%A")
            if weekday in ["Понедельник", "Среда", "Пятница"]:
                score += 15
            
            # Определяем тип дня
            if score > 70:
                day_type = "🌟 Очень благоприятный"
            elif score > 50:
                day_type = "⭐ Благоприятный"
            elif score > 30:
                day_type = "⚖️ Нейтральный"
            else:
                day_type = "⚠️ Неблагоприятный"
            
            best_dates.append({
                'date': current_date.strftime("%d.%m.%Y"),
                'weekday': weekday,
                'score': score,
                'day_type': day_type,
                'lunar_day': moon_phase['lunar_day'],
                'phase': moon_phase['phase_name'],
                'lunar_day_name': lunar_day_info['name'] if lunar_day_info else ""
            })
            
            current_date += timedelta(days=1)
        
        # Сортируем по убыванию оценки
        best_dates.sort(key=lambda x: x['score'], reverse=True)
        
        return best_dates[:10]  # Возвращаем топ-10 дат

class LunarWordAnalyzer:
    """Анализатор слов в контексте лунного календаря"""
    
    def __init__(self):
        self.lunar_calendar = LunarCalendar()
        self.word_categories = {
            'действие': ['сделать', 'начать', 'построить', 'создать'],
            'общение': ['сказать', 'поговорить', 'обсудить', 'поделиться'],
            'творчество': ['написать', 'нарисовать', 'спеть', 'придумать'],
            'анализ': ['подумать', 'проанализировать', 'изучить', 'исследовать'],
            'отдых': ['отдохнуть', 'расслабиться', 'помедитировать', 'поспать']
        }
    
    def analyze_word_for_moon_phase(self, word, date=None):
        """Анализирует слово в контексте текущей лунной фазы"""
        if date is None:
            date = datetime.now()
        
        moon_phase = self.lunar_calendar.calculate_moon_phase(date)
        lunar_influence = self.lunar_calendar.word_to_lunar_influence(word, date)
        
        # Определяем категорию слова
        word_category = self._categorize_word(word)
        
        # Даём рекомендации в зависимости от фазы и категории
        phase = moon_phase['phase_percent']
        recommendations = []
        
        if phase < 25:  # Растущая Луна
            if word_category in ['действие', 'творчество']:
                recommendations.append("Идеальное время для действий, связанных с этим словом")
            recommendations.append("Начинайте новые проекты")
            recommendations.append("Загадывайте желания, связанные со словом")
        
        elif phase < 50:  # Первая четверть
            recommendations.append("Время активной реализации")
            recommendations.append("Преодолевайте препятствия")
            recommendations.append("Ищите поддержку")
        
        elif phase < 75:  # Полнолуние
            recommendations.append("Пик влияния слова")
            recommendations.append("Время осознания и понимания")
            recommendations.append("Проявляйте слово в действии")
        
        else:  # Убывающая Луна
            if word_category in ['анализ', 'отдых']:
                recommendations.append("Лучшее время для работы с этим словом")
            recommendations.append("Завершайте дела, связанные со словом")
            recommendations.append("Избавляйтесь от ненужного")
        
        # Добавляем общие рекомендации
        recommendations.append(f"Лунный день {moon_phase['lunar_day']}: {lunar_influence['lunar_day_info']['advice']}")
        
        return {
            'word': word,
            'category': word_category,
            'moon_phase': moon_phase,
            'lunar_influence': lunar_influence,
            'recommendations': recommendations,
            'best_time': "Утро" if phase < 50 else "Вечер",
            'element': self._get_element_for_word(word)
        }
    
    def _categorize_word(self, word):
        """Определяет категорию слова"""
        word_lower = word.lower()
        for category, words in self.word_categories.items():
            if word_lower in words:
                return category
        
        # Если слово не найдено, определяем по характеристикам
        if any(char in word_lower for char in ['ть', 'чь', 'стить']):  # Глаголы
            return 'действие'
        elif any(char in word_lower for char in ['ов', 'ев', 'ин']):  # Прилагательные
            return 'описание'
        else:
            return 'общее'
    
    def _get_element_for_word(self, word):
        """Определяет стихию для слова"""
        # Простая система: по первой букве
        elements = {
            'а': 'Огонь', 'б': 'Земля', 'в': 'Воздух', 'г': 'Вода',
            'д': 'Огонь', 'е': 'Земля', 'ё': 'Воздух', 'ж': 'Вода',
            'з': 'Огонь', 'и': 'Земля', 'й': 'Воздух', 'к': 'Вода',
            'л': 'Огонь', 'м': 'Земля', 'н': 'Воздух', 'о': 'Вода',
            'п': 'Огонь', 'р': 'Земля', 'с': 'Воздух', 'т': 'Вода',
            'у': 'Огонь', 'ф': 'Земля', 'х': 'Воздух', 'ц': 'Вода',
            'ч': 'Огонь', 'ш': 'Земля', 'щ': 'Воздух', 'ъ': 'Вода',
            'ы': 'Огонь', 'ь': 'Земля', 'э': 'Воздух', 'ю': 'Вода',
            'я': 'Огонь'
        }
        first_char = word[0].lower() if word else 'а'
        return elements.get(first_char, 'Смешанная')

def main_lunar_menu():
    """Главное меню лунного календаря"""
    lunar = LunarCalendar()
    analyzer = LunarWordAnalyzer()
    
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║          ЛУННЫЙ КАЛЕНДАРЬ СЛОВ                        ║
    ║  Связь слов с фазами Луны и лунными днями            ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "="*70)
        print("ЛУННОЕ МЕНЮ:")
        print("1. Текущая фаза Луны и лунный день")
        print("2. Анализ слова в контексте Луны")
        print("3. Лунный календарь на месяц")
        print("4. Найти лучшую дату для слова")
        print("5. Лунный гороскоп слова")
        print("6. Анализ нескольких слов")
        print("7. Выход")
        print("="*70)
        
        choice = input("\nВыберите действие (1-7): ").strip()
        
        if choice == "1":
            date_str = input("Введите дату (ГГГГ-ММ-ДД или Enter для текущей): ").strip()
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    date = datetime.now()
                    print("Неверный формат, использую текущую дату")
            else:
                date = datetime.now()
            
            moon_phase = lunar.calculate_moon_phase(date)
            lunar_pos = lunar.calculate_lunar_position(date)
            lunar_day_info = lunar.get_lunar_day_info(moon_phase['lunar_day'])
            
            print(f"\n📅 Дата: {date.strftime('%d.%m.%Y')}")
            print(f"🌙 Фаза Луны: {moon_phase['phase_name']}")
            print(f"📊 Заполненность: {moon_phase['phase_percent']:.1f}%")
            print(f"🔢 Лунный день: {moon_phase['lunar_day']} - {lunar_day_info['name']}")
            print(f"   Энергия: {lunar_day_info['energy']}")
            print(f"   Совет: {lunar_day_info['advice']}")
            print(f"♋ Луна в знаке: {lunar_pos['sign']} {lunar_pos['symbol']}")
            print(f"   {lunar_pos['description']}")
            
            # Показываем символ лунного дня
            print(f"\n{'='*30}")
            for i in range(1, 31):
                if i == moon_phase['lunar_day']:
                    print(f"[{lunar.get_lunar_day_symbol(i)}]", end=" ")
                else:
                    print(f" {lunar.get_lunar_day_symbol(i)} ", end=" ")
                if i % 10 == 0:
                    print()
            print(f"{'='*30}")
            print(f"   Сегодня: день {moon_phase['lunar_day']}")
        
        elif choice == "2":
            word = input("Введите слово: ").strip()
            date_str = input("Введите дату (ГГГГ-ММ-ДД или Enter для текущей): ").strip()
            
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    date = datetime.now()
            else:
                date = datetime.now()
            
            analysis = analyzer.analyze_word_for_moon_phase(word, date)
            
            print(f"\n{'='*70}")
            print(f"АНАЛИЗ СЛОВА: '{word.upper()}'")
            print(f"Дата: {date.strftime('%d.%m.%Y')}")
            print(f"{'='*70}")
            
            print(f"\n🌙 ЛУННЫЕ ХАРАКТЕРИСТИКИ:")
            print(f"  Фаза: {analysis['moon_phase']['phase_name']}")
            print(f"  Лунный день: {analysis['moon_phase']['lunar_day']}")
            print(f"  Луна в знаке: {analysis['lunar_influence']['lunar_sign']}")
            
            print(f"\n📊 ВЛИЯНИЕ НА СЛОВО:")
            print(f"  Уровень влияния: {analysis['lunar_influence']['influence_type']}")
            print(f"  Эффект: {analysis['lunar_influence']['effect']}")
            print(f"  Стихия слова: {analysis['element']}")
            
            print(f"\n💡 РЕКОМЕНДАЦИИ:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            print(f"\n⏰ Лучшее время суток: {analysis['best_time']}")
            
            # Показываем график влияния
            influence = analysis['lunar_influence']['influence_level']
            bar_length = int(influence * 40)
            print(f"\n📈 ГРАФИК ВЛИЯНИЯ:")
            print(f"  [{'█' * bar_length}{'░' * (40-bar_length)}] {influence*100:.1f}%")
        
        elif choice == "3":
            date_str = input("Введите начальную дату (ГГГГ-ММ-ДД или Enter для текущей): ").strip()
            if date_str:
                try:
                    start_date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    start_date = datetime.now()
            else:
                start_date = datetime.now()
            
            days = 30
            calendar = lunar.generate_lunar_calendar(start_date, days)
            
            print(f"\n📅 ЛУННЫЙ КАЛЕНДАРЬ НА {days} ДНЕЙ")
            print(f"Начало: {start_date.strftime('%d.%m.%Y')}")
            print("="*80)
            print(f"{'Дата':<12} {'День':<10} {'Лун.день':<10} {'Фаза':<20} {'Знак':<12} {'%':<6}")
            print("-"*80)
            
            for day in calendar:
                print(f"{day['date']:<12} {day['day_of_week'][:3]:<10} "
                      f"{day['lunar_day']:<10} {day['moon_phase'][:20]:<20} "
                      f"{day['lunar_sign'][:10]:<12} {day['phase_percent']:<6.1f}")
            
            # Сохранение календаря
            save = input("\nСохранить календарь в файл? (да/нет): ").strip().lower()
            if save in ['да', 'д', 'yes', 'y']:
                filename = f"lunar_calendar_{start_date.strftime('%Y%m%d')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Лунный календарь с {start_date.strftime('%d.%m.%Y')}\n")
                    f.write("="*80 + "\n")
                    for day in calendar:
                        f.write(f"{day['date']} | {day['day_of_week']:>10} | "
                                f"Лунный день: {day['lunar_day']:>2} | "
                                f"Фаза: {day['moon_phase']:>20} | "
                                f"Знак: {day['lunar_sign']}\n")
                print(f"Календарь сохранён в {filename}")
        
        elif choice == "4":
            word = input("Введите слово: ").strip()
            date_str = input("Введите начальную дату (ГГГГ-ММ-ДД или Enter для текущей): ").strip()
            
            if date_str:
                try:
                    start_date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    start_date = datetime.now()
            else:
                start_date = datetime.now()
            
            best_dates = lunar.find_best_date_for_word(word, start_date, 60)
            
            print(f"\n🌟 ЛУЧШИЕ ДАТЫ ДЛЯ СЛОВА '{word.upper()}'")
            print(f"Период поиска: 60 дней с {start_date.strftime('%d.%m.%Y')}")
            print("="*90)
            print(f"{'Дата':<12} {'День':<10} {'Оценка':<10} {'Тип дня':<25} {'Лун.день':<10} {'Фаза':<15}")
            print("-"*90)
            
            for i, date_info in enumerate(best_dates, 1):
                print(f"{i:2}. {date_info['date']:<12} {date_info['weekday'][:3]:<10} "
                      f"{date_info['score']:<10} {date_info['day_type']:<25} "
                      f"{date_info['lunar_day']:<10} {date_info['phase'][:15]}")
            
            print("\n💡 Совет: Запланируйте важные действия, связанные со словом, на эти даты")
        
        elif choice == "5":
            word = input("Введите слово для лунного гороскопа: ").strip()
            
            # Создаём "гороскоп" на основе хеша слова
            word_hash = hashlib.sha256(word.encode()).hexdigest()
            hash_numbers = [int(word_hash[i:i+2], 16) for i in range(0, len(word_hash), 2)]
            
            print(f"\n🔮 ЛУННЫЙ ГОРОСКОП ДЛЯ СЛОВА: '{word.upper()}'")
            print("="*70)
            
            # Аспекты слова
            aspects = [
                ("Прошлое слова", hash_numbers[0] % 12),
                ("Настоящее слова", hash_numbers[1] % 12),
                ("Будущее слова", hash_numbers[2] % 12),
                ("Сильная сторона", hash_numbers[3] % 12),
                ("Слабая сторона", hash_numbers[4] % 12),
                ("Совет Луны", hash_numbers[5] % 12)
            ]
            
            lunar_signs = [sign[0] for sign in lunar.lunar_signs]
            
            for aspect_name, sign_index in aspects:
                sign = lunar_signs[sign_index]
                print(f"  {aspect_name}: {sign}")
            
            # Лунные циклы для слова
            print(f"\n🌒 ЛУННЫЕ ЦИКЛЫ СЛОВА:")
            cycles = [
                ("Новолуние", "Начало влияния", hash_numbers[6] % 30 + 1),
                ("Полнолуние", "Пик влияния", hash_numbers[7] % 30 + 1),
                ("Затмение", "Трансформация", hash_numbers[8] % 30 + 1)
            ]
            
            for phase, meaning, day in cycles:
                print(f"  {phase}: {meaning} (лучше в лунные дни {day}-{day+3})")
            
            # Совместимость с фазами
            print(f"\n💫 СОВМЕСТИМОСТЬ:")
            compatibility = hash_numbers[9] % 100
            if compatibility > 80:
                print(f"  Отличная совместимость с лунными ритмами ({compatibility}%)")
            elif compatibility > 60:
                print(f"  Хорошая совместимость с лунными ритмами ({compatibility}%)")
            elif compatibility > 40:
                print(f"  Средняя совместимость с лунными ритмами ({compatibility}%)")
            else:
                print(f"  Слабая совместимость с лунными ритмами ({compatibility}%)")
        
        elif choice == "6":
            print("Введите несколько слов через запятую:")
            words_input = input("Слова: ").strip()
            words = [w.strip() for w in words_input.split(',') if w.strip()]
            
            if not words:
                print("Не введено ни одного слова!")
                continue
            
            date_str = input("Введите дату (ГГГГ-ММ-ДД или Enter для текущей): ").strip()
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    date = datetime.now()
            else:
                date = datetime.now()
            
            print(f"\n📊 СРАВНИТЕЛЬНЫЙ АНАЛИЗ СЛОВ")
            print(f"Дата: {date.strftime('%d.%m.%Y')}")
            print("="*90)
            print(f"{'Слово':<15} {'Категория':<12} {'Влияние':<15} {'Стихия':<10} {'Рекомендация':<30}")
            print("-"*90)
            
            analyses = []
            for word in words:
                analysis = analyzer.analyze_word_for_moon_phase(word, date)
                analyses.append(analysis)
                
                print(f"{word:<15} {analysis['category']:<12} "
                      f"{analysis['lunar_influence']['influence_type']:<15} "
                      f"{analysis['element']:<10} "
                      f"{analysis['recommendations'][0][:30]}")
            
            # Находим лучшее слово для сегодня
            best_word = max(analyses, 
                           key=lambda x: x['lunar_influence']['influence_level'])
            
            print(f"\n🌟 ЛУЧШЕЕ СЛОВО НА СЕГОДНЯ: '{best_word['word'].upper()}'")
            print(f"   Уровень влияния: {best_word['lunar_influence']['influence_level']*100:.1f}%")
            print(f"   {best_word['recommendations'][0]}")
        
        elif choice == "7":
            print("\nДо свидания! Пусть Луна освещает ваш путь! 🌙")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 7.")
        
        input("\nНажмите Enter для продолжения...")

# Интеграция с основной программой звёздных карт
def integrate_with_star_map():
    """Интегрирует лунный календарь со звёздной картой"""
    print("\n" + "="*70)
    print("ИНТЕГРАЦИЯ: ЛУННЫЙ КАЛЕНДАРЬ + ЗВЁЗДНАЯ КАРТА")
    print("="*70)
    
    lunar = LunarCalendar()
    
    # Получаем текущую фазу Луны
    moon_phase = lunar.calculate_moon_phase()
    lunar_pos = lunar.calculate_lunar_position()
    
    print(f"\n🌙 ТЕКУЩАЯ ЛУНА:")
    print(f"  Фаза: {moon_phase['phase_name']}")
    print(f"  Лунный день: {moon_phase['lunar_day']}")
    print(f"  Знак: {lunar_pos['sign']} {lunar_pos['symbol']}")
    
    print(f"\n🌟 ВЛИЯНИЕ НА ЗВЁЗДНЫЕ КАРТЫ:")
    
    # Определяем влияние на звёздные карты
    if moon_phase['phase_percent'] < 25:
        print("  Растущая Луна: благоприятное время для создания новых карт")
        print("  Энергия роста помогает проявиться новым звёздам-словам")
    elif moon_phase['phase_percent'] < 50:
        print("  Первая четверть: время активной работы с картами")
        print("  Добавляйте новые слова, расширяйте созвездия")
    elif moon_phase['phase_percent'] < 75:
        print("  Полнолуние: пик видимости звёздных карт")
        print("  Идеальное время для анализа и медитации на картах")
    else:
        print("  Убывающая Луна: время очистки и реорганизации карт")
        print("  Удаляйте ненужные слова, обновляйте структуры")
    
    # Связь с лунным днём
    lunar_day_info = lunar.get_lunar_day_info(moon_phase['lunar_day'])
    print(f"\n📅 ЛУННЫЙ ДЕНЬ {moon_phase['lunar_day']}:")
    print(f"  {lunar_day_info['name']}")
    print(f"  Энергия: {lunar_day_info['energy']}")
    print(f"  Совет для работы со словами: {lunar_day_info['advice']}")
    
    return {
        'moon_phase': moon_phase,
        'lunar_position': lunar_pos,
        'lunar_day_info': lunar_day_info
    }

if __name__ == "__main__":
    main_lunar_menu()
EOF