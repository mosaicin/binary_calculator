
class WordCalculator:
    def __init__(self):
        # Русский алфавит с двузначными кодами
        self.alphabet = {
            'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 'е': 6, 'ё': 7, 'ж': 8, 'з': 9, 'и': 10,
            'й': 11, 'к': 12, 'л': 13, 'м': 14, 'н': 15, 'о': 16, 'п': 17, 'р': 18, 'с': 19, 
            'т': 20, 'у': 21, 'ф': 22, 'х': 23, 'ц': 24, 'ч': 25, 'ш': 26, 'щ': 27, 'ъ': 28,
            'ы': 29, 'ь': 30, 'э': 31, 'ю': 32, 'я': 33,
            # Заглавные буквы
            'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9, 'И': 10,
            'Й': 11, 'К': 12, 'Л': 13, 'М': 14, 'Н': 15, 'О': 16, 'П': 17, 'Р': 18, 'С': 19,
            'Т': 20, 'У': 21, 'Ф': 22, 'Х': 23, 'Ц': 24, 'Ч': 25, 'Ш': 26, 'Щ': 27, 'Ъ': 28,
            'Ы': 29, 'Ь': 30, 'Э': 31, 'Ю': 32, 'Я': 33
        }
        
    def word_to_code(self, word):
        """Переводит слово в двузначные коды"""
        codes = []
        for letter in word:
            if letter in self.alphabet:
                code = self.alphabet[letter]
                # Форматируем как двузначное число (01, 02, ...)
                codes.append(f"{code:02d}")
            else:
                # Для символов не из алфавита используем 00
                codes.append("00")
        return codes
    
    def calculate_word_value(self, word, operation="sum"):
        """Вычисляет значение слова по выбранной операции"""
        codes = []
        numeric_codes = []
        
        for letter in word:
            if letter in self.alphabet:
                code = self.alphabet[letter]
                codes.append(f"{code:02d}")
                numeric_codes.append(code)
            else:
                codes.append("00")
                numeric_codes.append(0)
        
        if not numeric_codes:
            return 0, []
        
        # Выполняем выбранную операцию
        if operation == "sum":
            result = sum(numeric_codes)
        elif operation == "average":
            result = sum(numeric_codes) / len(numeric_codes)
        elif operation == "product":
            result = 1
            for num in numeric_codes:
                result *= num if num > 0 else 1
        elif operation == "min":
            result = min([num for num in numeric_codes if num > 0]) if any(numeric_codes) else 0
        elif operation == "max":
            result = max(numeric_codes)
        else:
            result = sum(numeric_codes)
        
        return result, codes
    
    def compare_words(self, word1, word2, operation="compare"):
        """Сравнивает два слова или выполняет операцию между ними"""
        val1, codes1 = self.calculate_word_value(word1, "sum")
        val2, codes2 = self.calculate_word_value(word2, "sum")
        
        results = {}
        
        if operation == "compare":
            results[f"{word1}"] = val1
            results[f"{word2}"] = val2
            results["разница"] = abs(val1 - val2)
            results["больше"] = word1 if val1 > val2 else word2 if val2 > val1 else "равны"
            
        elif operation == "add":
            results["сумма"] = val1 + val2
            
        elif operation == "subtract":
            results["разность"] = val1 - val2
            
        elif operation == "multiply":
            results["произведение"] = val1 * val2
            
        elif operation == "divide":
            if val2 != 0:
                results["частное"] = val1 / val2
            else:
                results["частное"] = "деление на ноль"
                
        return results
    
    def print_menu(self):
        """Выводит меню программы"""
        print("\n" + "="*50)
        print("ПРОГРАММА 'СЛОВОКАЛЬКУЛЯТОР'")
        print("="*50)
        print("1. Перевести слово в двузначный код")
        print("2. Вычислить сумму кодов слова")
        print("3. Вычислить среднее значение кодов")
        print("4. Найти минимальный/максимальный код")
        print("5. Сравнить два слова")
        print("6. Выполнить арифметику между словами")
        print("7. Показать таблицу кодов букв")
        print("8. Выход")
        print("="*50)
    
    def show_alphabet_table(self):
        """Показывает таблицу соответствия букв и кодов"""
        print("\nТАБЛИЦА КОДОВ:")
        print("-"*30)
        print("Буква | Код | Буква | Код")
        print("-"*30)
        
        # Сортируем русские буквы
        russian_letters = sorted([(k, v) for k, v in self.alphabet.items() 
                                 if k in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'], 
                                 key=lambda x: x[1])
        
        # Выводим в два столбца
        for i in range(0, len(russian_letters), 2):
            letter1, code1 = russian_letters[i]
            line = f"  {letter1.upper()}/{letter1}  | {code1:02d}"
            
            if i + 1 < len(russian_letters):
                letter2, code2 = russian_letters[i + 1]
                line += f"   |  {letter2.upper()}/{letter2}  | {code2:02d}"
            
            print(line)
        print("-"*30)

def main():
    calculator = WordCalculator()
    
    while True:
        calculator.print_menu()
        
        try:
            choice = input("\nВыберите действие (1-8): ").strip()
            
            if choice == "1":
                word = input("Введите слово: ").strip()
                codes = calculator.word_to_code(word)
                print(f"\nСлово: {word}")
                print(f"Коды: {' '.join(codes)}")
                print(f"Последовательность: {''.join(codes)}")
                
            elif choice == "2":
                word = input("Введите слово: ").strip()
                result, codes = calculator.calculate_word_value(word, "sum")
                print(f"\nСлово: {word}")
                print(f"Коды: {' '.join(codes)}")
                print(f"Сумма кодов: {result}")
                
            elif choice == "3":
                word = input("Введите слово: ").strip()
                result, codes = calculator.calculate_word_value(word, "average")
                print(f"\nСлово: {word}")
                print(f"Коды: {' '.join(codes)}")
                print(f"Среднее значение: {result:.2f}")
                
            elif choice == "4":
                word = input("Введите слово: ").strip()
                min_val, codes = calculator.calculate_word_value(word, "min")
                max_val, _ = calculator.calculate_word_value(word, "max")
                print(f"\nСлово: {word}")
                print(f"Коды: {' '.join(codes)}")
                print(f"Минимальный код: {min_val}")
                print(f"Максимальный код: {max_val}")
                
            elif choice == "5":
                word1 = input("Введите первое слово: ").strip()
                word2 = input("Введите второе слово: ").strip()
                results = calculator.compare_words(word1, word2, "compare")
                
                print(f"\nСравнение слов:")
                print(f"'{word1}': сумма = {results[word1]}")
                print(f"'{word2}': сумма = {results[word2]}")
                print(f"Разница: {results['разница']}")
                print(f"Большее значение: '{results['больше']}'")
                
            elif choice == "6":
                print("\nОперации между словами:")
                print("1. Сложение сумм")
                print("2. Вычитание сумм")
                print("3. Умножение сумм")
                print("4. Деление сумм")
                op_choice = input("Выберите операцию (1-4): ").strip()
                
                word1 = input("Введите первое слово: ").strip()
                word2 = input("Введите второе слово: ").strip()
                
                operations = {"1": "add", "2": "subtract", "3": "multiply", "4": "divide"}
                operation = operations.get(op_choice, "add")
                
                results = calculator.compare_words(word1, word2, operation)
                val1, _ = calculator.calculate_word_value(word1, "sum")
                val2, _ = calculator.calculate_word_value(word2, "sum")
                
                print(f"\nОперация над словами:")
                print(f"'{word1}': сумма = {val1}")
                print(f"'{word2}': сумма = {val2}")
                
                for key, value in results.items():
                    print(f"{key}: {value}")
                    
            elif choice == "7":
                calculator.show_alphabet_table()
                
            elif choice == "8":
                print("\nВыход из программы. До свидания!")
                break
                
            else:
                print("\nНеверный выбор. Попробуйте снова.")
                
            # Пауза перед следующим действием
            input("\nНажмите Enter для продолжения...")
            
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
EOF
