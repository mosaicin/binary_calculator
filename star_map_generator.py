
import math
import hashlib
from datetime import datetime
import json
import os

class StarMapGenerator:
    def __init__(self):
        # Создаём базовую звёздную карту (созвездия и яркие звёзды)
        self.constellations = {
            'Большая Медведица': {
                'stars': [(12.5, 55), (13.0, 56), (13.5, 57), (13.5, 58), 
                         (14.0, 58.5), (14.5, 59), (15.0, 60)],
                'lines': [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6)],
                'color': 'cyan'
            },
            'Орион': {
                'stars': [(5.5, -5), (5.5, -7), (6.0, -1), (6.0, -8), 
                         (6.5, -2), (6.5, -6)],
                'lines': [(0,2), (2,4), (1,3), (3,5)],
                'color': 'yellow'
            },
            'Кассиопея': {
                'stars': [(1.0, 60), (1.5, 58), (2.0, 60), (2.5, 55), (3.0, 58)],
                'lines': [(0,1), (1,2), (2,3), (3,4)],
                'color': 'magenta'
            }
        }
        
        # Яркие звёзды (RA в часах, Dec в градусах, название)
        self.bright_stars = [
            (6.752, -16.716, 'Сириус'),
            (5.242, -8.202, 'Ригель'),
            (5.919, 7.407, 'Бетельгейзе'),
            (10.140, 11.967, 'Регул'),
            (14.660, -60.834, 'Альфа Центавра'),
            (19.846, 8.868, 'Альтаир'),
            (18.616, 38.784, 'Вега'),
            (2.530, 89.264, 'Полярная')
        ]
        
    def word_to_binary(self, word):
        """Переводит слово в двоичный код"""
        binary = ''
        try:
            for char in word.encode('utf-8'):
                binary += format(char, '08b')
        except:
            # Если ошибка, используем простую кодировку
            for char in word:
                binary += format(ord(char), '08b')
        return binary
    
    def binary_to_coordinates(self, binary_string):
        """Преобразует двоичный код в небесные координаты (RA, Dec)"""
        if not binary_string:
            return 0, 0
        
        # Используем хеш для получения координат
        # RA (прямое восхождение): 0-24 часа
        # Dec (склонение): -90 до +90 градусов
        
        # Создаём хеш из двоичной строки
        hash_obj = hashlib.sha256(binary_string.encode() if isinstance(binary_string, str) else binary_string)
        hash_hex = hash_obj.hexdigest()
        
        # Берём части хеша для RA и Dec
        ra_hash = int(hash_hex[:8], 16)  # первые 8 hex символов
        dec_hash = int(hash_hex[8:16], 16)  # следующие 8
        
        # Преобразуем в координаты
        ra_hours = (ra_hash / (16**8)) * 24  # 0-24 часа
        dec_degrees = (dec_hash / (16**8)) * 180 - 90  # -90 до +90 градусов
        
        return ra_hours, dec_degrees
    
    def coordinates_to_star_name(self, ra, dec):
        """Находит ближайшую яркую звезду к данным координатам"""
        min_distance = float('inf')
        closest_star = None
        
        for star_ra, star_dec, name in self.bright_stars:
            # Простое евклидово расстояние в 2D
            distance = math.sqrt((ra - star_ra)**2 + (dec - star_dec)**2)
            if distance < min_distance:
                min_distance = distance
                closest_star = (star_ra, star_dec, name, distance)
        
        return closest_star
    
    def create_star_from_word(self, word, word_id=1):
        """Создаёт 'звезду' из слова"""
        binary = self.word_to_binary(word)
        ra, dec = self.binary_to_coordinates(binary)
        
        # Находим ближайшую реальную звезду
        closest = self.coordinates_to_star_name(ra, dec)
        
        # Создаём уникальную звезду для слова
        star = {
            'id': word_id,
            'word': word,
            'binary': binary[:64] + '...' if len(binary) > 64 else binary,
            'binary_length': len(binary),
            'coordinates': {
                'ra_hours': ra,
                'dec_degrees': dec,
                'ra_formatted': self.hours_to_hms(ra),
                'dec_formatted': self.degrees_to_dms(dec)
            },
            'closest_star': {
                'name': closest[2] if closest else None,
                'distance_deg': closest[3] if closest else None
            },
            'magnitude': self.calculate_magnitude(word),  # Видимая звёздная величина
            'color': self.word_to_color(word),
            'constellation': self.assign_to_constellation(ra, dec)
        }
        
        return star
    
    def calculate_magnitude(self, word):
        """Вычисляет 'видимую звёздную величину' на основе слова"""
        # Чем длиннее слово и чем больше в нём редких букв, тем ярче
        length_factor = len(word) / 10  # нормализуем
        vowel_count = sum(1 for c in word.lower() if c in 'аеёиоуыэюя')
        rarity_factor = (len(word) - vowel_count) / len(word) if word else 0
        
        # Яркость от -1 (очень яркая) до 6 (едва видимая)
        magnitude = 6 - (length_factor * 3 + rarity_factor * 4)
        return round(max(-1, min(6, magnitude)), 2)
    
    def word_to_color(self, word):
        """Определяет цвет звезды на основе слова"""
        # Используем хеш для определения цвета
        colors = ['белый', 'голубой', 'синий', 'жёлтый', 'оранжевый', 'красный']
        hash_val = hash(word) % len(colors)
        return colors[hash_val]
    
    def assign_to_constellation(self, ra, dec):
        """Привязывает к созвездию по координатам"""
        for name, data in self.constellations.items():
            # Простая проверка: если координаты в районе созвездия
            stars_ra = [star[0] for star in data['stars']]
            stars_dec = [star[1] for star in data['stars']]
            
            min_ra, max_ra = min(stars_ra), max(stars_ra)
            min_dec, max_dec = min(stars_dec), max(stars_dec)
            
            if min_ra <= ra <= max_ra and min_dec <= dec <= max_dec:
                return name
        
        return "Созвездие Слов"
    
    def hours_to_hms(self, hours):
        """Преобразует часы в формат ЧЧ:ММ:СС"""
        total_seconds = hours * 3600
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def degrees_to_dms(self, degrees):
        """Преобразует градусы в формат ГГ:ММ:СС"""
        sign = '-' if degrees < 0 else '+'
        abs_deg = abs(degrees)
        d = int(abs_deg)
        m = int((abs_deg - d) * 60)
        s = int(((abs_deg - d) * 60 - m) * 60)
        return f"{sign}{d:02d}°{m:02d}'{s:02d}\""
    
    def generate_star_map(self, words, save_to_file=False):
        """Генерирует звёздную карту для списка слов"""
        stars = []
        
        print("\n" + "="*70)
        print("ГЕНЕРАЦИЯ ЗВЁЗДНОЙ КАРТЫ СЛОВ")
        print("="*70)
        
        for i, word in enumerate(words, 1):
            star = self.create_star_from_word(word, i)
            stars.append(star)
            
            # Выводим информацию о созданной звезде
            print(f"\n🌟 ЗВЕЗДА #{i}: '{word}'")
            print(f"   Координаты: RA {star['coordinates']['ra_formatted']}, "
                  f"Dec {star['coordinates']['dec_formatted']}")
            print(f"   Созвездие: {star['constellation']}")
            print(f"   Цвет: {star['color']}, Зв. величина: {star['magnitude']}")
            print(f"   Ближайшая реальная звезда: {star['closest_star']['name']}")
            print(f"   Двоичный код: {star['binary'][:32]}...")
        
        # Создаём текстовую карту
        print("\n" + "="*70)
        print("ТЕКСТОВАЯ ЗВЁЗДНАЯ КАРТА")
        print("="*70)
        
        # Простая текстовая визуализация
        self.print_text_star_map(stars)
        
        # Сохраняем в файл если нужно
        if save_to_file:
            self.save_star_map(words, stars)
        
        return stars
    
    def print_text_star_map(self, stars):
        """Печатает текстовую звёздную карту"""
        # Создаём сетку 40x20 для отображения
        grid = [[' ' for _ in range(60)] for _ in range(20)]
        
        # Размещаем звёзды на сетке
        for star in stars:
            # Преобразуем координаты в координаты сетки
            # RA: 0-24 часа -> 0-60 столбцов
            # Dec: -90+90 -> 0-20 строк
            x = int((star['coordinates']['ra_hours'] / 24) * 58)
            y = int(((star['coordinates']['dec_degrees'] + 90) / 180) * 18)
            
            # Ограничиваем координаты
            x = max(0, min(58, x))
            y = max(0, min(18, y))
            
            # Определяем символ в зависимости от яркости
            magnitude = star['magnitude']
            if magnitude < 0:
                symbol = '★'  # Очень яркая
            elif magnitude < 2:
                symbol = '☆'  # Яркая
            elif magnitude < 4:
                symbol = '⭑'  # Средняя
            else:
                symbol = '∙'  # Тусклая
            
            # Размещаем символ на сетке
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                grid[y][x] = symbol
        
        # Печатаем сетку с координатами
        print("\n    Прямое восхождение (RA) 0h → 24h")
        print("   " + "─" * 60)
        
        for i, row in enumerate(grid):
            # Подписываем склонение
            dec = 90 - (i * 10)
            label = f"{dec:+3d}°"
            print(f"{label} │ " + ''.join(row) + " │")
        
        print("   " + "─" * 60)
        print("    Склонение (Dec) +90° → -90°")
        
        # Легенда
        print("\nЛегенда:")
        print("★ - Очень яркая (зв. величина < 0)")
        print("☆ - Яркая (0-2)")
        print("⭑ - Средняя (2-4)")
        print("∙ - Тусклая (>4)")
    
    def save_star_map(self, words, stars):
        """Сохраняет звёздную карту в файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"star_map_{timestamp}.json"
        
        star_map_data = {
            'generated': datetime.now().isoformat(),
            'words': words,
            'stars': stars,
            'constellations': list(self.constellations.keys()),
            'bright_stars': [star[2] for star in self.bright_stars]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(star_map_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Звёздная карта сохранена в файл: {filename}")
        
        # Также создаём текстовый отчёт
        self.save_text_report(words, stars, timestamp)
    
    def save_text_report(self, words, stars, timestamp):
        """Создаёт текстовый отчёт о звёздной карте"""
        filename = f"star_map_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ЗВЁЗДНАЯ КАРТА СЛОВ - ОТЧЁТ\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write(f"Количество слов: {len(words)}\n\n")
            
            f.write("СЛОВА И ИХ ЗВЁЗДЫ:\n")
            f.write("-"*70 + "\n")
            
            for star in stars:
                f.write(f"\nЗвезда #{star['id']}: '{star['word']}'\n")
                f.write(f"  Координаты: RA {star['coordinates']['ra_formatted']}, "
                       f"Dec {star['coordinates']['dec_formatted']}\n")
                f.write(f"  Созвездие: {star['constellation']}\n")
                f.write(f"  Цвет: {star['color']}\n")
                f.write(f"  Видимая звёздная величина: {star['magnitude']}\n")
                f.write(f"  Ближайшая реальная звезда: {star['closest_star']['name']} "
                       f"(расстояние: {star['closest_star']['distance_deg']:.2f}°)\n")
                f.write(f"  Двоичный код ({star['binary_length']} бит): {star['binary'][:80]}...\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("КАК ЧИТАТЬ КАРТУ:\n")
            f.write("-"*70 + "\n")
            f.write("RA (Прямое восхождение) - аналог долготы на небе, измеряется в часах (0-24)\n")
            f.write("Dec (Склонение) - аналог широты на небе, измеряется в градусах (-90 до +90)\n")
            f.write("Звёздная величина: чем меньше число, тем звезда ярче\n")
            f.write("  - <0: очень яркие (как Сириус)\n")
            f.write("  - 0-2: яркие (видны в городе)\n")
            f.write("  - 2-4: средние (видны за городом)\n")
            f.write("  - >4: тусклые (нужен телескоп)\n")
        
        print(f"📄 Текстовый отчёт сохранён в: {filename}")

def main():
    generator = StarMapGenerator()
    
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║          ЗВЁЗДНАЯ КАРТА СЛОВ                         ║
    ║  Преобразует слова в звёзды на небесной сфере        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "="*70)
        print("МЕНЮ:")
        print("1. Создать звёздную карту для списка слов")
        print("2. Добавить слово к существующей карте")
        print("3. Показать информацию о конкретной звезде")
        print("4. Справка о координатах и звёздных величинах")
        print("5. Выход")
        print("="*70)
        
        choice = input("\nВыберите действие (1-5): ").strip()
        
        if choice == "1":
            print("\nВведите слова для создания звёздной карты.")
            print("Можно ввести несколько слов через запятую или каждое с новой строки.")
            print("Завершите ввод пустой строкой.")
            
            words = []
            while True:
                line = input("Слово (или Enter для завершения): ").strip()
                if not line:
                    break
                
                # Разделяем строку на слова
                line_words = [w.strip() for w in line.split(',') if w.strip()]
                words.extend(line_words)
            
            if not words:
                print("Не введено ни одного слова!")
                continue
            
            save = input("Сохранить карту в файл? (да/нет): ").strip().lower()
            save_to_file = save in ['да', 'д', 'yes', 'y']
            
            generator.generate_star_map(words, save_to_file)
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "2":
            word = input("Введите новое слово: ").strip()
            if not word:
                print("Слово не может быть пустым!")
                continue
            
            # Просто создаём звезду для одного слова
            star = generator.create_star_from_word(word, 1)
            
            print(f"\n🌟 НОВАЯ ЗВЕЗДА: '{word}'")
            print(f"   Координаты: RA {star['coordinates']['ra_formatted']}, "
                  f"Dec {star['coordinates']['dec_formatted']}")
            print(f"   Созвездие: {star['constellation']}")
            print(f"   Цвет: {star['color']}, Зв. величина: {star['magnitude']}")
            print(f"   Ближайшая реальная звезда: {star['closest_star']['name']}")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "3":
            word = input("Введите слово для анализа: ").strip()
            if not word:
                print("Слово не может быть пустым!")
                continue
            
            star = generator.create_star_from_word(word, 1)
            
            print(f"\n" + "="*70)
            print(f"АНАЛИЗ ЗВЕЗДЫ ДЛЯ СЛОВА: '{word}'")
            print("="*70)
            
            print(f"\n📍 КООРДИНАТЫ:")
            print(f"   Прямое восхождение (RA): {star['coordinates']['ra_formatted']}")
            print(f"   Склонение (Dec): {star['coordinates']['dec_formatted']}")
            print(f"   (RA: {star['coordinates']['ra_hours']:.4f} ч, "
                  f"Dec: {star['coordinates']['dec_degrees']:.4f}°)")
            
            print(f"\n🎨 ХАРАКТЕРИСТИКИ:")
            print(f"   Созвездие: {star['constellation']}")
            print(f"   Цвет: {star['color']}")
            print(f"   Видимая звёздная величина: {star['magnitude']}")
            
            print(f"\n🔭 БЛИЖАЙШИЕ ОБЪЕКТЫ:")
            print(f"   Ближайшая яркая звезда: {star['closest_star']['name']}")
            print(f"   Угловое расстояние: {star['closest_star']['distance_deg']:.2f}°")
            
            print(f"\n💾 ДВОИЧНЫЙ КОД:")
            print(f"   Длина: {star['binary_length']} бит")
            print(f"   Первые 80 бит: {star['binary'][:80]}")
            
            # Показываем положение на мини-карте
            print(f"\n🗺️  ПОЛОЖЕНИЕ НА КАРТЕ:")
            print(f"   (Используйте эти координаты в программах типа Stellarium)")
            print(f"   Координаты для Stellarium: RA={star['coordinates']['ra_hours']:.6f}h, "
                  f"Dec={star['coordinates']['dec_degrees']:.6f}°")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "4":
            print("\n" + "="*70)
            print("СПРАВКА: НЕБЕСНЫЕ КООРДИНАТЫ")
            print("="*70)
            
            print("""
            📍 СИСТЕМА КООРДИНАТ:
            
            • RA (Прямое восхождение) - аналог долготы на Земле
              - Измеряется в часах, минутах и секундах (0h до 24h)
              - 1 час = 15 градусов, 1 минута = 15 угловых минут
            
            • Dec (Склонение) - аналог широты на Земле
              - Измеряется в градусах, минутах и секундах (-90° до +90°)
              - 0° = небесный экватор, +90° = северный полюс, -90° = южный полюс
            
            🌟 ЗВЁЗДНАЯ ВЕЛИЧИНА:
            
            • Чем МЕНЬШЕ число, тем звезда ЯРЧЕ
            • Шкала логарифмическая: разница в 1 величину = яркость отличается в ~2.5 раза
            
            Примеры:
            - -1.5: Очень яркая (Сириус: -1.46)
            - 0: Яркая (Вега: 0.03)
            - 2-3: Видны в городе
            - 4-5: Видны за городом
            - 6: Предел видимости невооружённым глазом
            
            🎨 ЦВЕТА ЗВЁЗД:
            
            • Голубой: >30,000°C (самые горячие)
            • Белый: 10,000-30,000°C
            • Жёлтый: 6,000-10,000°C (как Солнце)
            • Оранжевый: 4,000-6,000°C
            • Красный: <4,000°C (самые холодные)
            """)
            
            print("\n🔭 ПРИМЕРЫ ЯРКИХ ЗВЁЗД:")
            for ra, dec, name in generator.bright_stars[:5]:
                print(f"   • {name}: RA={ra:.2f}h, Dec={dec:.2f}°")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "5":
            print("\nДо свидания! Пусть ваши звёзды светят ярко! 🌟")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    main()
EOF
