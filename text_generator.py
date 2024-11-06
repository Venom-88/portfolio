# -*- coding: utf-8 -*-

import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

# Шаблоны для разных разделов
templates = {
    'catalog-vagonka': '''<p>{product_name_full}</p><p>Интернет-магазин «Дядя Юра» представляет: {product_name_base} собственного производства по низким ценам. Для заказа выберите подходящий:</p><ul><li>размер пиломатериалов, например, {dimensions} мм;</li><li>вид и сорт древесины;</li><li>профиль;</li><li>применение — для обычных помещений, либо для парных.</li></ul><p>Продукция нашего бренда отличается высокой стойкостью к гниению, поэтому вы сможете использовать вагонку для отделки помещений с повышенным уровнем влажности. Наши менеджеры помогут подобрать материалы под конкретный проект, а также согласовать все необходимые опции по доставке заказа.</p>''',

    'catalog-blok-haus': '''<p>{product_name_full}</p><p>В каталоге интернет-магазина «Дядя Юра» представлен качественный {product_name_base} из различных видов древесины собственного изготовления, например, {wood_type}. Мы предлагаем доступные цены и качество от производителя, а также дополнительные услуги — выпуск пиломатериалов нестандартного размера и распиловку под ваш проект. Для оформления заказа выберите подходящий размер: {dimensions} мм, а также сорт — к примеру, {grade}, учитывая условия эксплуатации. При возникновении любых вопросов по заказу обращайтесь к нашим менеджерам на сайте или по телефону.</p>''',

    'catalog-imitaciya-brusa': '''<p>{product_name_full}</p><p>{product_name_base} в интернет-магазине «Дядя Юра» представлена в большом ассортименте видов древесины и сортов. Продукция нашего производства отличается высоким качеством, стойкостью к перепадам температуры и гниению под воздействием высокой влажности, а также повышенными показателями шумо- и теплоизоляции. Вы сможете использовать имитацию бруса из {wood_type} размера: {dimensions} и влажностью {humidity}% для облицовки фасадов и интерьеров. Наши менеджеры по телефону и на сайте помогут с комплектацией заказа, а также с согласованием опций по доставке и дополнительным услугам (например, распиловкой под проект).</p>''',

    'catalog-planken': '''<p>{product_name_full}</p><p>Интернет-магазин «Дядя Юра» приглашает заказать {product_name_base} {profile_type} из {wood_type} подходящего размера: {dimensions}. Продукция нашего производства соответствует ГОСТ, прекрасно сопротивляется неблагоприятным факторам — повышенной влажности, перепадам температуры. Планкен подходит для всех видов наружных и внутренних отделочных работ, а также для строительства беседок, лестниц, террас. Наши менеджеры помогут выбрать пиломатериалы, подходящие под ваш проект, рассчитать стоимость заказа и согласовать доставку. Также вы можете забрать покупку самостоятельно с нашего склада в Москве.</p>''',

    'doska-chetvert-1': '''<p>{product_name_full}</p><p>Интернет-магазин «Дядя Юра» поставляет {product_name_base_accusative} собственного производства из {wood_type}, соответствующую ГОСТ 8486-86. Выберите размер: {dimensions}, а также {grade}. Продукция обладает стойкостью к повышенной влажности, а также к поражению плесенью и жучками. Доска-четверть подходит для внешних и внутренних отделочных работ, строительства. Благодаря точной геометрии торцевого профиля вы получите идеальную стыковку досок без подгонки. Для согласования опций доставки и других вопросов по заказу обращайтесь к нашим менеджерам — на сайте, либо по телефону.</p>''',

    'catalog-shpuntovanaya-doska': '''<p>{product_name_full}</p><p>{product_name_base} производства компании «Дядя Юра» — это качественный пиломатериал из {wood_type}, соответствующий ГОСТ 8242-88. При оформлении заказа выберите подходящий сорт, к примеру — {grade} и размер: {dimensions}, а также необходимые дополнительные опции — у нас можно заказать точный распил под ваш проект. Мы поставляем строганные шпунтованные доски различной влажности. Укажите ту, которая подходит для ваших целей и задач, например, {humidity}%. Вопросы по заказу помогут согласовать наши менеджеры — воспользуйтесь для этого удобной формой связи на сайте или позвоните нам по телефону.</p>''',

    'evropol': '''<p>{product_name_full}</p><p>Заказать {product_name_base} по доступной цене приглашает интернет-магазин «Дядя Юра». Мы изготавливаем пиломатериалы стандартных размеров, укажите необходимый для вашего проекта, например: {thickness} х {width} х {length}{grade_text}. Также у нас можно заказать партию по своим замерам — для согласования технического задания обратитесь к нашим менеджерам по телефону или на сайте. Европол — современный и долговечный тип напольного покрытия, который подходит для отделочных работ в жилых и других помещениях. Мы гарантируем точность размеров пиломатериалов и предоставляем сертификат качества!</p>''',

    'parketnaja-doska': '''<p>{product_name_full}</p><p>{product_name_base} производства компании «Дядя Юра» — качественное напольное покрытие, которое вы можете заказать из подходящей под ваш проект древесины — например, {wood_type}. Выберите из представленного ассортимента подходящий размер: {length} х {width} х {thickness}, а также укажите дополнительные параметры — влажность {humidity}% и {grade}. Также обратите внимание на применение — мы предлагаем материалы для укладки в банях и парных, достаточно указать соответствующую опцию при оформлении заказа. Согласовать вопросы по заказу вам помогут менеджеры интернет-магазина на сайте или по телефону.</p>''',
}

# Функция для определения раздела на основе названия товара
def determine_section(name):
    name_lower = name.lower()
    if 'вагонка' in name_lower:
        return 'catalog-vagonka'
    elif 'блок-хаус' in name_lower or 'блок хаус' in name_lower:
        return 'catalog-blok-haus'
    elif 'имитация бруса' in name_lower:
        return 'catalog-imitaciya-brusa'
    elif 'планкен' in name_lower or 'штакетник' in name_lower:
        return 'catalog-planken'
    elif 'доска-четверть' in name_lower or 'доска четверть' in name_lower:
        return 'doska-chetvert-1'
    elif 'шпунтованная доска' in name_lower:
        return 'catalog-shpuntovanaya-doska'
    elif 'европол' in name_lower:
        return 'evropol'
    elif 'паркетная доска' in name_lower:
        return 'parketnaja-doska'
    else:
        return 'unknown'

# Функция для парсинга данных из названия товара
def parse_product_name(name):
    # Инициализация значений по умолчанию
    dimensions = 'не указаны'
    thickness = 'не указана'
    width = 'не указана'
    length = 'не указана'
    humidity = 'не указана'
    wood_type = 'не указан'
    wood_type_nominative = 'не указан'
    grade = 'не указан'
    profile_type = 'не указан'
    product_name_full = name.strip()
    product_name_base = 'не указано'
    product_name_base_accusative = 'не указано'
    sauna_suitable = 'нет'  # Новая переменная для применения в банях и парных

    # Удаляем лишние пробелы и приводим к единому формату
    name = name.strip()

    # Словарь базовых понятий товара с их номинативными формами
    base_terms = {
        'евровагонка': 'Евровагонка',
        'вагонка штиль сращ': 'Вагонка штиль сращенная',
        'вагонка штиль сращенная': 'Вагонка штиль сращенная',
        'вагонка штиль': 'Вагонка штиль',
        'вагонка': 'Вагонка',
        'блок-хаус': 'Блок-хаус',
        'блок хаус': 'Блок-хаус',
        'имитация бруса': 'Имитация бруса',
        'планкен': 'Планкен',
        'штакетник': 'Планкен',
        'доска-четверть': 'Доска-четверть',
        'доска четверть': 'Доска-четверть',
        'шпунтованная доска': 'Шпунтованная доска',
        'европол': 'Европол',
        'паркетная доска': 'Паркетная доска'
    }

    # Сортируем ключи по длине в обратном порядке, чтобы сначала обрабатывать более длинные
    sorted_base_terms = dict(sorted(base_terms.items(), key=lambda item: -len(item[0])))

    # Поиск базового понятия товара
    for term_lower, term_nominative in sorted_base_terms.items():
        pattern = r'\b' + re.escape(term_lower) + r'\b'
        if re.search(pattern, name.lower()):
            product_name_base = term_nominative
            # Удаляем базовое понятие из названия товара
            name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
            break

    # Словарь форм базовых понятий (именительный и винительный падежи)
    product_name_base_cases = {
        'Евровагонка': 'Евровагонку',
        'Вагонка': 'Вагонку',
        'Вагонка штиль': 'Вагонку штиль',
        'Вагонка штиль сращенная': 'Вагонку штиль сращенную',
        'Блок-хаус': 'Блок-хаус',
        'Имитация бруса': 'Имитацию бруса',
        'Планкен': 'Планкен',
        'Доска-четверть': 'Доску-четверть',
        'Шпунтованная доска': 'Шпунтованную доску',
        'Европол': 'Европол',
        'Паркетная доска': 'Паркетную доску'
    }

    # Получаем винительную форму базового понятия
    product_name_base_accusative = product_name_base_cases.get(product_name_base, product_name_base)

    # Поиск размеров с поддержкой дробных чисел
    dimensions_pattern = r'(\d+(?:[.,]\d+)?[xх×]\d+(?:[.,]\d+)?(?:[xх×]\d+(?:[.,]\d+)?)?)(?:\s*мм)?'
    dimensions_match = re.search(dimensions_pattern, name, re.IGNORECASE)
    section = determine_section(product_name_full)
    if dimensions_match:
        dimensions = dimensions_match.group(1)
        # Заменяем разделители на 'x' и удаляем 'мм'
        dimensions_clean = re.sub(r'[хХ×]', 'x', dimensions)
        dimensions_clean = dimensions_clean.replace('мм', '').strip()
        dimensions = dimensions_clean.replace(',', '.')  # Заменяем запятые на точки
        # Убираем размеры из названия товара
        name = name.replace(dimensions_match.group(0), '').strip()
        # Split dimensions into components
        dimensions_list = dimensions.split('x')
        if section == 'parketnaja-doska':
            if len(dimensions_list) == 3:
                length, width, thickness = dimensions_list
            elif len(dimensions_list) == 2:
                length, width = dimensions_list
                thickness = 'не указана'
            else:
                # Handle other cases if necessary
                pass
        else:
            if len(dimensions_list) == 3:
                thickness, width, length = dimensions_list
            elif len(dimensions_list) == 2:
                thickness, width = dimensions_list
                length = 'не указана'
            else:
                # Handle other cases if necessary
                pass
        # Append 'мм' to each dimension
        thickness = thickness.strip() + ' мм' if thickness != 'не указана' else 'не указана'
        width = width.strip() + ' мм' if width != 'не указана' else 'не указана'
        length = length.strip() + ' мм' if length != 'не указана' else 'не указана'
    else:
        dimensions = 'не указаны'
        thickness = 'не указана'
        width = 'не указана'
        length = 'не указана'

    # Поиск влажности
    humidity_pattern = r'(?:влажность\s*([0-9]+%?))'
    humidity_match = re.search(humidity_pattern, name, re.IGNORECASE)
    if humidity_match:
        humidity = humidity_match.group(1).strip('%')
        name = re.sub(humidity_pattern, '', name, flags=re.IGNORECASE).strip()

    # Составляем словарь видов древесины с вариантами написания
    wood_variants = {
        'Ангарская сосна': ['ангарская сосна', 'ангарской сосны', 'ангарская', 'ангарск'],
        'Термососна': ['термососна', 'термососны', 'термо сосна', 'термо-сосна', 'термо сосны', 'термо-сосны'],
        'Термолиственница': ['термолиственница', 'термо-лиственница', 'термо лиственница', 'термолиственницы'],
        'Лиственница': ['лиственниц', 'лиственница', 'лиственнице', 'лиственницу', 'лиственницей', 'лиственницах', 'лиственницы'],
        'Сосна': ['сосна', 'сосны', 'сосне', 'сосну', 'сосной', 'соснах'],
        'Дуб': ['дуб', 'дуба', 'дубе', 'дубу', 'дубом', 'дубах', 'дубы'],
        'Ель': ['ель', 'ели', 'елю', 'елью', 'елями', 'елях'],
        'Осина': ['осина', 'осины', 'осине', 'осину', 'осиной', 'осинах'],
        'Ольха': ['ольха', 'ольхи', 'ольхе', 'ольху', 'ольхой', 'ольхах'],
        'Ясень': ['ясень', 'ясеня', 'ясеню', 'ясенем', 'ясенях'],
        'Кедр': ['кедр', 'кедра', 'кедру', 'кедром', 'кедре', 'кедрах', 'кедры'],
        'Липа': ['липа', 'липы', 'липе', 'липу', 'липой', 'липами', 'липах'],
        'Хвоя': ['хвоя', 'хвои', 'хвое', 'хвою', 'хвоей', 'хвоях'],
    }

    # Поиск вида древесины
    for wood, variants in wood_variants.items():
        for variant in variants:
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, name.lower()):
                wood_type_nominative = wood  # Сохраняем в именительном падеже
                # Преобразование wood_type в родительный падеж
                wood_genitive = {
                    'Лиственница': 'Лиственницы',
                    'Сосна': 'Сосны',
                    'Термососна': 'Термососны',
                    'Термолиственница': 'Термолиственницы',
                    'Дуб': 'Дуба',
                    'Ель': 'Ели',
                    'Ангарская сосна': 'Ангарской сосны',
                    'Осина': 'Осины',
                    'Ольха': 'Ольхи',
                    'Ясень': 'Ясеня',
                    'Кедр': 'Кедра',
                    'Липа': 'Липы',
                    'Хвоя': 'Хвои',
                }
                wood_type = wood_genitive.get(wood, wood)
                # Удаляем вид древесины из названия товара
                name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
                break
        if wood_type != 'не указан':
            break

    # Присваиваем значение влажности на основе wood_type_nominative, если она не была указана ранее
    if humidity == 'не указана':
        wood_humidity = {
            'Лиственница': '14',
            'Сосна': '14',
            'Термососна': '3-4',
            'Термолиственница': '3-4',
            'Дуб': '8-10',
            'Липа': '8-12',
            'Ольха': '8-10',
            'Ель': '14',
            'Кедр': '14',
            'Осина': '12',
            'Хвоя': '12-15',
            'Ангарская сосна': '12-14',
            # Добавьте другие виды древесины и их влажность по мере необходимости
        }
        if wood_type_nominative in wood_humidity:
            humidity = wood_humidity[wood_type_nominative]

    # Поиск типа профиля для планкена
    if 'планкен' in product_name_base.lower():
        profile_types = {
            'прямой': ['прямой', 'прямой профиль'],
            'скошенный': ['скошенный', 'скошенный профиль'],
            'радиусный': ['радиусный', 'радиусный профиль'],
            # Добавьте другие типы профилей, если необходимо
        }
        for profile, variants in profile_types.items():
            for variant in variants:
                pattern = r'\b' + re.escape(variant) + r'\b'
                if re.search(pattern, name.lower()):
                    profile_type = profile.capitalize()
                    # Удаляем тип профиля из названия товара
                    name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
                    break
            if profile_type != 'не указан':
                break
        # Если тип профиля не указан, то по умолчанию 'Прямой'
        if profile_type == 'не указан':
            profile_type = 'Прямой'

    # Также ищем тип профиля для штакетника
    if 'штакетник' in product_name_full.lower():
        profile_types = {
            'прямой': ['прямой', 'прямой профиль'],
            'скошенный': ['скошенный', 'скошенный профиль'],
            'фигурный': ['фигурный', 'фигурный профиль'],
            # Добавьте другие типы профилей, если необходимо
        }
        for profile, variants in profile_types.items():
            for variant in variants:
                pattern = r'\b' + re.escape(variant) + r'\b'
                if re.search(pattern, name.lower()):
                    profile_type = profile.capitalize()
                    # Удаляем тип профиля из названия товара
                    name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
                    break
            if profile_type != 'не указан':
                break
        # Если тип профиля не указан, то по умолчанию 'Прямой'
        if profile_type == 'не указан':
            profile_type = 'Прямой'

    # Поиск сорта
    grade_pattern = r'(?:сорт\s*([A-Za-zА-Яа-я0-9\-]+))'
    grade_match = re.search(grade_pattern, name, re.IGNORECASE)
    if grade_match:
        grade = 'сорт ' + grade_match.group(1).strip()
        name = re.sub(r'сорт\s*' + re.escape(grade_match.group(1)), '', name, flags=re.IGNORECASE).strip()
    else:
        possible_grades = ['Ex0', 'A', 'B', 'AB', 'А', 'В', 'Прима', 'Экстра', '0-1', '1-3']
        for pg in possible_grades:
            pattern = r'\b' + re.escape(pg.lower()) + r'\b'
            if re.search(pattern, name.lower()):
                grade = 'сорт ' + pg
                name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
                break

    # Adjust grade for template
    if grade != 'не указан':
        grade_text = ' и ' + grade
    else:
        grade_text = ''

    # Определяем, подходит ли продукт для бань и парных
    if re.search(r'\b(баня|парная|сауна|для бани|для парной|для сауны)\b', name.lower()):
        sauna_suitable = 'да'
        name = re.sub(r'\b(баня|парная|сауна|для бани|для парной|для сауны)\b', '', name, flags=re.IGNORECASE).strip()
    else:
        sauna_suitable = 'нет'

    # Убираем лишние пробелы
    name = re.sub(r'\s{2,}', ' ', name).strip()

    return {
        'product_name_full': product_name_full,
        'product_name_base': product_name_base,
        'product_name_base_accusative': product_name_base_accusative,
        'dimensions': dimensions,
        'thickness': thickness,
        'width': width,
        'length': length,
        'humidity': humidity,
        'wood_type': wood_type,
        'grade': grade,
        'grade_text': grade_text,
        'profile_type': profile_type,
        'sauna_suitable': sauna_suitable,  # Добавляем новый параметр в возвращаемый словарь
    }

# Функция для генерации описания и сохранения в текстовый файл
def generate_descriptions():
    product_list = text_area.get("1.0", tk.END).strip().split('\n')
    output_folder = 'product_descriptions'
    os.makedirs(output_folder, exist_ok=True)
    descriptions = []
    skipped_products = []  # Список для хранения пропущенных товаров
    for product_name in product_list:
        if not product_name.strip():
            continue

        # Определяем раздел
        section = determine_section(product_name)

        if section == 'unknown':
            skipped_products.append((product_name, "Не удалось определить раздел"))
            continue

        if section not in templates:
            skipped_products.append((product_name, f"Для раздела '{section}' нет шаблона"))
            continue

        # Парсим название товара
        parsed_data = parse_product_name(product_name)

        # Удаляем лишние пробелы в базовом названии
        parsed_data['product_name_base'] = parsed_data['product_name_base'].strip()

        # Проверка на наличие необходимых данных
        if parsed_data['wood_type'] == 'не указан' and section != 'evropol':
            skipped_products.append((product_name, "Не удалось определить вид древесины"))
            continue

        # Получаем шаблон для раздела
        template = templates[section]

        # Подставляем данные в шаблон
        try:
            description = template.format(**parsed_data)
            # Заменяем символы перевода строки на пробелы
            description = description.replace('\n', ' ')
        except KeyError as e:
            skipped_products.append((product_name, f"Не удалось подставить значение для {e}"))
            continue

        # Добавляем описание в список
        descriptions.append(description)

    if not descriptions:
        messagebox.showinfo("Нет описаний", "Не удалось сгенерировать описания для введенных товаров.")
        return

    # Объединяем все описания, разделяя их переводом строки
    final_output = '\n'.join(descriptions)
    # Сохранение всех описаний в текстовый файл с расширением .txt
    txt_file_path = os.path.join(output_folder, 'product_descriptions.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txtfile:
        txtfile.write(final_output)

    # Сохранение пропущенных товаров в отдельный файл
    if skipped_products:
        skipped_file_path = os.path.join(output_folder, 'skipped_products.txt')
        with open(skipped_file_path, 'w', encoding='utf-8') as skippedfile:
            for product_name, reason in skipped_products:
                skippedfile.write(f"{product_name} - {reason}\n")
        messagebox.showinfo("Готово", f"Описания товаров сохранены в файле '{txt_file_path}'.\n"
                                      f"Некоторые товары были пропущены. Подробнее см. в '{skipped_file_path}'")
    else:
        messagebox.showinfo("Готово", f"Описания товаров сохранены в файле '{txt_file_path}'.\n")

# Создание графического интерфейса
root = tk.Tk()
root.title("Генератор описаний товаров")

tk.Label(root, text="Введите список товаров (по одному на строке):").pack(pady=5)

text_area = scrolledtext.ScrolledText(root, width=80, height=20)
text_area.pack(pady=5)

# Добавление контекстного меню
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Копировать", command=lambda: text_area.event_generate("<<Copy>>"))
context_menu.add_command(label="Вставить", command=lambda: text_area.event_generate("<<Paste>>"))

text_area.bind("<Button-3>", show_context_menu)

generate_button = tk.Button(root, text="Сгенерировать описания", command=generate_descriptions)
generate_button.pack(pady=10)

root.mainloop()
