class BinaryWordCalculator:
    def __init__(self):
        # Кодировка по умолчанию - UTF-8
        self.encoding = 'utf-8'
        
    def word_to_binary(self, word, encoding='utf-8'):
        """Переводит слово в двоичный код (0 и 1)"""
        try:
            # Кодируем слово в байты
            bytes_data = word.encode(encoding)
            
            # Преобразуем каждый байт в двоичную строку
            binary_string = ''
            for byte in bytes_data:
                binary_string += format(byte, '08b')  # 8 бит с ведущими нулями
            
            return binary_string
        except UnicodeEncodeError:
            print(f"Ошибка: Невозможно закодировать слово в {encoding}")
            return ""
    
    def binary_to_word(self, binary_string, encoding='utf-8'):
        """Переводит двоичный код обратно в слово"""
        try:
            # Проверяем, что длина строки кратна 8
            if len(binary_string) % 8 != 0:
                print("Ошибка: Длина двоичной строки должна быть кратна 8")
                return ""
            
            # Разбиваем строку на байты (по 8 символов)
            bytes_list = []
            for i in range(0, len(binary_string), 8):
                byte_str = binary_string[i:i+8]
                byte_value = int(byte_str, 2)
                bytes_list.append(byte_value)
            
            # Преобразуем байты в строку
            bytes_data = bytes(bytes_list)
            return bytes_data.decode(encoding)
        except (ValueError, UnicodeDecodeError) as e:
            print(f"Ошибка при декодировании: {e}")
            return ""
    
    def calculate_binary_value(self, binary_string, operation="sum"):
        """Выполняет операции с двоичной строкой"""
        if not binary_string:
            return 0
        
        # Преобразуем двоичную строку в целое число
        numeric_value = int(binary_string, 2)
        
        # Считаем статистику
        stats = {
            "длина_бит": len(binary_string),
            "количество_1": binary_string.count('1'),
            "количество_0": binary_string.count('0'),
            "числовое_значение": numeric_value
        }
        
        return stats
    
    def binary_operations(self, binary1, binary2, operation="xor"):
        """Выполняет бинарные операции между двумя двоичными строками"""
        # Приводим к одинаковой длине, добавляя ведущие нули
        max_len = max(len(binary1), len(binary2))
        bin1 = binary1.zfill(max_len)
        bin2 = binary2.zfill(max_len)
        
        result = ""
        
        if operation == "xor":
            for b1, b2 in zip(bin1, bin2):
                result += '1' if b1 != b2 else '0'
        
        elif operation == "and":
            for b1, b2 in zip(bin1, bin2):
                result += '1' if b1 == '1' and b2 == '1' else '0'
        
        elif operation == "or":
            for b1, b2 in zip(bin1, bin2):
                result += '1' if b1 == '1' or b2 == '1' else '0'
        
        elif operation == "add":
            # Арифметическое сложение чисел
            num1 = int(binary1, 2) if binary1 else 0
            num2 = int(binary2, 2) if binary2 else 0
            result = format(num1 + num2, 'b')
        
        elif operation == "subtract":
            num1 = int(binary1, 2) if binary1 else 0
            num2 = int(binary2, 2) if binary2 else 0
            result = format(max(num1 - num2, 0), 'b')
        
        return result
    
    def analyze_binary_pattern(self, binary_string):
        """Анализирует паттерны в двоичной строке"""
        if not binary_string:
            return {}
        
        analysis = {
            "общая_длина": len(binary_string),
            "байтов": len(binary_string) // 8,
            "бит_1": binary_string.count('1'),
            "бит_0": binary_string.count('0'),
            "соотношение_1_0": f"{binary_string.count('1')}:{binary_string.count('0')}",
            "процент_1": f"{(binary_string.count('1') / len(binary_string) * 100):.1f}%",
            "самая_длинная_последовательность_1": max(map(len, binary_string.split('0'))),
            "самая_длинная_последовательность_0": max(map(len, binary_string.split('1')))
        }
        
        # Группируем по байтам
        bytes_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
        analysis["байты"] = bytes_list
        
        return analysis
    
    def visualize_binary(self, binary_string, bytes_per_line=4):
        """Визуализирует двоичный код в виде таблицы"""
        if not binary_string:
            print("Пустая строка")
            return
        
        bytes_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
        
        print("\n" + "="*60)
        print("ВИЗУАЛИЗАЦИЯ ДВОИЧНОГО КОДА")
        print("="*60)
        
        for i in range(0, len(bytes_list), bytes_per_line):
            line_bytes = bytes_list[i:i+bytes_per_line]
            
            # Выводим байты
            print(f"\nБайты {i//bytes_per_line + 1}:")
            print("  ".join(f"[{j+1:2d}] {byte}" for j, byte in enumerate(line_bytes)))
            
            # Выводим десятичные значения
            print("Десятичные: ", end="")
            for byte in line_bytes:
                if byte:
                    print(f"{int(byte, 2):3d} ", end="")
            print()
            
            # Визуализация
            print("Визуально:   ", end="")
            for byte in line_bytes:
                for bit in byte:
                    print("█" if bit == '1' else "░", end="")
                print(" ", end="")
            print()
    
    def print_menu(self):
        """Выводит меню программы"""
        print("\n" + "="*60)
        print("БИНАРНЫЙ КАЛЬКУЛЯТОР СЛОВ (0 и 1)")
        print("="*60)
        print("1. Перевести слово в двоичный код (UTF-8)")
        print("2. Перевести двоичный код обратно в слово")
        print("3. Анализ двоичного кода (статистика)")
        print("4. Визуализировать двоичный код")
        print("5. Бинарные операции между двумя словами")
        print("6. Сравнить двоичные коды двух слов")
        print("7. Изменить кодировку (сейчас: UTF-8)")
        print("8. Примеры и демонстрация")
        print("9. Выход")
        print("="*60)

def main():
    calculator = BinaryWordCalculator()
    
    # Примеры для демонстрации
    examples = {
        "привет": "Пример: 'привет' в двоичном коде",
        "охота": "Пример: 'охота' в двоичном коде", 
        "hello": "Пример: английское 'hello'",
        "мир": "Короткое слово 'мир'"
    }
    
    while True:
        calculator.print_menu()
        
        try:
            choice = input("\nВыберите действие (1-9): ").strip()
            
            if choice == "1":
                word = input("Введите слово: ").strip()
                binary = calculator.word_to_binary(word, calculator.encoding)
                
                if binary:
                    print(f"\nСлово: '{word}'")
                    print(f"Кодировка: {calculator.encoding}")
                    print(f"Двоичный код ({len(binary)} бит):")
                    
                    # Форматируем вывод с пробелами между байтами
                    formatted = ' '.join([binary[i:i+8] for i in range(0, len(binary), 8)])
                    print(formatted)
                    
                    # Краткая статистика
                    stats = calculator.calculate_binary_value(binary)
                    print(f"\nСтатистика:")
                    print(f"  Всего бит: {stats['длина_бит']}")
                    print(f"  Единиц (1): {stats['количество_1']}")
                    print(f"  Нулей (0): {stats['количество_0']}")
                    print(f"  Десятичное значение: {stats['числовое_значение']}")
            
            elif choice == "2":
                binary_input = input("Введите двоичный код (только 0 и 1): ").strip()
                # Убираем возможные пробелы
                binary_input = binary_input.replace(" ", "")
                
                if all(bit in '01' for bit in binary_input):
                    word = calculator.binary_to_word(binary_input, calculator.encoding)
                    if word:
                        print(f"\nДвоичный код восстановлен как слово: '{word}'")
                else:
                    print("Ошибка: Двоичный код должен содержать только 0 и 1")
            
            elif choice == "3":
                binary_input = input("Введите двоичный код или слово: ").strip()
                
                # Если введено не двоичное число, конвертируем слово
                if not all(bit in '01' for bit in binary_input.replace(" ", "")):
                    binary = calculator.word_to_binary(binary_input, calculator.encoding)
                    print(f"Слово '{binary_input}' преобразовано в двоичный код")
                else:
                    binary = binary_input.replace(" ", "")
                
                if binary:
                    analysis = calculator.analyze_binary_pattern(binary)
                    
                    print(f"\nАНАЛИЗ ДВОИЧНОГО КОДА ({len(binary)} бит):")
                    print("-"*40)
                    for key, value in analysis.items():
                        if key != "байты":
                            print(f"{key.replace('_', ' ').title()}: {value}")
                    
                    # Показываем первые несколько байт
                    if "байты" in analysis and analysis["байты"]:
                        print(f"\nПервые 5 байт:")
                        for i, byte in enumerate(analysis["байты"][:5]):
                            print(f"  Байт {i+1}: {byte} = {int(byte, 2)} десятичное")
            
            elif choice == "4":
                word = input("Введите слово для визуализации: ").strip()
                binary = calculator.word_to_binary(word, calculator.encoding)
                
                if binary:
                    calculator.visualize_binary(binary)
                    
                    # Дополнительная информация
                    print(f"\nДополнительно:")
                    print(f"Слово: '{word}'")
                    print(f"Количество байт: {len(binary)//8}")
                    print(f"Общее количество бит: {len(binary)}")
            
            elif choice == "5":
                word1 = input("Введите первое слово: ").strip()
                word2 = input("Введите второе слово: ").strip()
                
                binary1 = calculator.word_to_binary(word1, calculator.encoding)
                binary2 = calculator.word_to_binary(word2, calculator.encoding)
                
                if binary1 and binary2:
                    print(f"\nСЛОВО 1: '{word1}'")
                    print(f"Двоичный: {binary1[:80]}..." if len(binary1) > 80 else f"Двоичный: {binary1}")
                    
                    print(f"\nСЛОВО 2: '{word2}'")
                    print(f"Двоичный: {binary2[:80]}..." if len(binary2) > 80 else f"Двоичный: {binary2}")
                    
                    print("\n" + "-"*40)
                    print("РЕЗУЛЬТАТЫ ОПЕРАЦИЙ:")
                    
                    operations = [
                        ("xor", "Исключающее ИЛИ"),
                        ("and", "Логическое И"),
                        ("or", "Логическое ИЛИ"),
                        ("add", "Арифметическая сумма"),
                    ]
                    
                    for op_code, op_name in operations:
                        result = calculator.binary_operations(binary1, binary2, op_code)
                        print(f"\n{op_name}:")
                        print(f"  Результат ({len(result)} бит): {result[:80]}..." if len(result) > 80 else f"  Результат: {result}")
                        
                        # Попробуем декодировать результат
                        decoded = calculator.binary_to_word(result, calculator.encoding)
                        if decoded:
                            print(f"  Декодировано как: '{decoded}'")
            
            elif choice == "6":
                word1 = input("Введите первое слово: ").strip()
                word2 = input("Введите второе слово: ").strip()
                
                binary1 = calculator.word_to_binary(word1, calculator.encoding)
                binary2 = calculator.word_to_binary(word2, calculator.encoding)
                
                if binary1 and binary2:
                    stats1 = calculator.calculate_binary_value(binary1)
                    stats2 = calculator.calculate_binary_value(binary2)
                    
                    print(f"\nСРАВНЕНИЕ ДВОИЧНЫХ КОДОВ:")
                    print("="*50)
                    print(f"{'Параметр':<30} '{word1}'    '{word2}'")
                    print("-"*50)
                    
                    parameters = [
                        ("Длина (бит)", "длина_бит"),
                        ("Количество единиц", "количество_1"),
                        ("Количество нулей", "количество_0"),
                        ("Десятичное значение", "числовое_значение"),
                    ]
                    
                    for param_name, param_key in parameters:
                        val1 = stats1[param_key]
                        val2 = stats2[param_key]
                        print(f"{param_name:<30} {val1:<10} {val2:<10}")
                    
                    # Сравнение визуально
                    print(f"\nВизуальное сравнение (первые 32 бита):")
                    print(f"'{word1}': {binary1[:32]}")
                    print(f"'{word2}': {binary2[:32]}")
                    
                    # Считаем сходство
                    min_len = min(len(binary1), len(binary2))
                    matches = sum(1 for i in range(min_len) if binary1[i] == binary2[i])
                    similarity = (matches / min_len) * 100
                    print(f"\nСходство битов: {similarity:.1f}%")
            
            elif choice == "7":
                print(f"\nТекущая кодировка: {calculator.encoding}")
                print("Доступные кодировки:")
                print("1. UTF-8 (рекомендуется, универсальная)")
                print("2. Windows-1251 (кириллица, 1 байт на символ)")
                print("3. ASCII (только английские буквы)")
                
                enc_choice = input("Выберите кодировку (1-3): ").strip()
                encodings = {"1": "utf-8", "2": "cp1251", "3": "ascii"}
                
                if enc_choice in encodings:
                    calculator.encoding = encodings[enc_choice]
                    print(f"Кодировка изменена на: {calculator.encoding}")
                else:
                    print("Неверный выбор, оставляем UTF-8")
            
            elif choice == "8":
                print("\nДЕМОНСТРАЦИОННЫЕ ПРИМЕРЫ:")
                print("-"*40)
                
                for word, description in examples.items():
                    binary = calculator.word_to_binary(word, calculator.encoding)
                    if binary:
                        print(f"\n{description}:")
                        print(f"Слово: '{word}'")
                        print(f"Двоичный код ({len(binary)} бит):")
                        
                        # Показываем первые 64 бита
                        preview = binary[:64] + "..." if len(binary) > 64 else binary
                        formatted = ' '.join([preview[i:i+8] for i in range(0, len(preview), 8)])
                        print(formatted)
                        
                        # Простая статистика
                        ones = binary.count('1')
                        zeros = binary.count('0')
                        print(f"Статистика: {ones} единиц, {zeros} нулей")
                
                print("\n" + "="*40)
                print("Пример бинарной операции XOR:")
                word1, word2 = "мир", "война"
                bin1 = calculator.word_to_binary(word1, calculator.encoding)
                bin2 = calculator.word_to_binary(word2, calculator.encoding)
                
                if bin1 and bin2:
                    result = calculator.binary_operations(bin1, bin2, "xor")
                    print(f"'{word1}' XOR '{word2}' = {result[:64]}...")
            
            elif choice == "9":
                print("\nВыход из программы. До свидания!")
                break
            
            else:
                print("Неверный выбор. Попробуйте снова.")
            
            # Пауза перед следующим действием
            input("\nНажмите Enter для продолжения...")
            
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()  
