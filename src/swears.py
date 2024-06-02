import re
from fuzzywuzzy import fuzz
from check_swear import SwearingCheck


class SFilter:
    def __init__(self):
        self.sch = SwearingCheck()

        self.patterns = [
            r'\bбл[яеё]+[тдцч]*[иыаоь]*',  # блять, бляди, блядь, блядская, бляцкий и т.д.
            r'ху[йиеёяю]+[нчвкгл]*[иеыао]*',  # хуй, хуиня, хуяк, хуета, хуячить и т.д.
            r'п[иеё]зд[аоы]*[цч]*[иеыа]*',  # пизда, пиздец, пиздеть, пиздюк и т.д.
            r'е[бп][аеёюяи]*[нщтн]*[ауоыыяеё]*',  # ебаный, ебать, ебнулся, еблан и т.д.
            r'м[уа]д[аеио]*[кзл]*',  # мудак, мудила, мудозвон и т.д.
            r'сук[аиоы]*',  # сука, суки и т.д.
            r'п[иеё]д[аео]р[аиоы]*',  # пидар, пидор и т.д.
            r'з[аеё]б[ауоыи]*[т]*[аиоы]*',  # заебал, заебись, заебенить и т.д.
            r'гандон[аиоы]*',  # гандон, гандонище и т.д.
            r'д[ао]лб[ао]е[бп][аиоы]*',  # долбоеб, долбоебина и т.д.
            r'мраз[ьиь]+[еиао]*',  # мразь, мразота и т.д.
            r'нах[уийе]*',  # нахуй, нахер и т.д.
            r'ёб[ареиь]*',  # ёбарь, ёбарь и т.д.
            r'шлю[хш][ауоыыяеё]*',  # шлюха, шлюхи и т.д.
            r'fuck[ing]*',  # fuck, fucking и т.д.
            r'shit[ty]*',  # shit, shitty и т.д.
            r'asshole',  # asshole
            r'bitch[es]*',  # bitch, bitches
            r'cunt',  # cunt
            r'motherfuck[ea]r[s]*',  # motherfucker, motherfuckers
            # Крылатые выражения
            r'иди[ть]* нахуй',  # иди нахуй
            r'пош[её]л на хуй',  # пошел на хуй
            r'ни х[уя][сз]ебе',  # нихуясе, нихуясебе
            r'еб[аеё]ный врот',  # ебаный врот
            r'еб[аеё]ть-колотить',  # ебать-колотить
            r'еб[аеё]на мать',  # ебена мать
            r'еб[аеё]твою мать',  # еб твою мать
            r'оху[еиё]т[ье]*',  # охуеть, охуительно
            r'вы[ие][бп][аеё]*',  # выебать, выебон и т.д.
            r'раз[ьъ][ьъеи]б[аеё]*',  # разъебать, разъебон и т.д.
            r'перее[бп][аеё]*',  # переебать, переебон и т.д.
            r'недое[бп][аеё]*',  # недоебать, недоебон и т.д.
            r'залуп[аыоие]*',  # залупа, залупы, залупе и т.д.
            r'дроч[иауы]*',  # дрочить, дрочила и т.д.
            r'выеб[аеё]*',  # выебать, выебон и т.д.
            r'хер[аио]*',  # хер, хера и т.д.
            r'поху[ие]*',  # похуй, похую и т.д.
            r'манда[вс]*',  # манда, мандовошка и т.д.
            r'потрах[аио]*',  # потрахаться, потрахал и т.д.
            r'трах[аиеёны]*',  # трах, траханье, трахыч
            r'снош[аио]*',  # сношаться, сношал и т.д.
            r'гнид[аиоеы]*',  # гнида, гниды и т.д.
            r'г[ао]вн[аио]*',  # говно, говнарь и т.д.
            r'высер[аио]*',  # высер, высеры и т.д.
            r'ублюд[аои]*',  # ублюдок, ублюдки и т.д.
            r'ебар[аиое]*',  # ебарь, ебара и т.д.
            r'педик[аио]*',  # педик, педика и т.д.
            r'мандов[аиое]*',  # мандовошка, мандовошки и т.д.
            r'залупиц[аеио]*',  # залупиться, залупается и т.д.
            r'выбляд[аио]*',  # выблядок, выблядки и т.д.
            r'ебыр[аиое]*',  # ебырь, ебыря и т.д.
            r'[сш]перм[аеёоу]*',  # сперма, шперма, спермы
            r'хули*',
            r'(?<!за)(?<!о)конч\w*',  # исключая закончил, окончил
        ]

        self.exact_patterns = [
            "сука", "сучка",
            "блять", "бляди", "блядь", "блядская", "бляцкий",
            "хуй", "хуиня", "хуяк", "хуета", "хуячить", "хуевина",
            "пизда", "пиздец", "пиздеть", "пиздюк",
            "ебаный", "ебать", "ебнулся", "еблан",
            "мудак", "мудила", "мудозвон",
            "пидар", "пидор", "пидр", "пидрила", "пидорас", "пидарас", "пидорасище",
            "заебал", "заебись", "заебенить",
            "гандон", "гандонище",
            "долбоеб", "долбоебина", "далбаеб", "долбаеб", "далбоеб",
            "мразь", "мразота",
            "залупа", "залупы", "залупе",
            "ублюдок", "ублюдки", "уебища", "уебище",
            "шлюха",
            "сперма",
            "хули",
            "манда", "мандовошка",
            "трах", "траханье", "трахаться",
            "дрочить", "дрочила",
            "выебать", "выебон",
            "похуй", "похую",
            "гнида", "гниды",
            "говно", "говнарь",
            "ублюдок", "ублюдки",
            "ебарь",
            "педик",
            "залупиться",
            "выблядок",
            "ебырь",
            "кончить",
            "гнида",
            "сперма",
            "хер",
            "похуист",
            "мандовошка"
        ]

        self.letter_map = {
            'а': r'[аa4]',
            'б': r'[бb6п]',
            'в': r'[вvb]',
            'г': r'[гg]',
            'д': r'[дd]',
            'е': r'[еeё3и1]',
            'ё': r'[ёe3]',
            'ж': r'[ж*]',
            'з': r'[з3z]',
            'и': r'[иi1!]',
            'й': r'[йi1!]',
            'к': r'[кk]',
            'л': r'[лl!^|1]',
            'м': r'[мm]',
            'н': r'[нnh]',
            'о': r'[оo0]',
            'п': r'[пnp]',
            'р': r'[рpr]',
            'с': r'[сcs]',
            'т': r'[тt]',
            'у': r'[уyu]',
            'ф': r'[фf]',
            'х': r'[хx]',
            'ц': r'[цu]',
            'ч': r'[ч4]',
            'ш': r'[шw]',
            'щ': r'[щw]',
            'ь': r'[ьb]',
            'ы': r'[ыbl]',
            'э': r'[э3]',
            'ю': r'[юu]',
            'я': r'[яr]'
        }

    def regex_check(self, text):
        cleared_text = self._clear(text.lower())

        for pattern in self.patterns:
            if re.findall(pattern, cleared_text):
                return True

        return self._advanced_check(cleared_text)

    def fuzzy_check(self, text):
        cleared_text = self._clear(text.lower())
        for pattern in self.exact_patterns:
            for word in cleared_text.split(" "):
                ratio = fuzz.ratio(word, pattern)
                if ratio >= 80:
                    return True
        return False

    def _convert_to_regex(self, word):
        regex_word = r'\b'
        for char in word:
            if char in self.letter_map:
                regex_word += self.letter_map[char]
            else:
                regex_word += char
        regex_word += r'*'
        return regex_word

    def neural_check(self, text):
        cleared_text = self._clear(text.lower())

        proba = self.sch.predict_proba(cleared_text)[0]

        percentage = round(proba, 4) * 100

        return percentage > 50

        # return percentage

    def _advanced_check(self, text):
        for exact_word in self.exact_patterns:
            regex_pattern = self._convert_to_regex(exact_word)
            if re.findall(regex_pattern, text):
                return True
        return False

    def _clear(self, text):

        text = text.replace(")(", "x")
        text = text.replace("><", "x")
        text = text.replace("@", "a")
        text = text.replace("/\\", "^")
        text = text.replace("/|", "^")
        text = text.replace("|\\", "^")
        text = text.replace("ё", "е")

        return ''.join(char for i, char in enumerate(text) if i == 0 or char != text[i - 1])


if __name__ == "__main__":
    # Пример использования
    sf = SFilter()

    texts = [
        "пиздец"
    ]

    for text in texts:
        print(f"(Регулярки) Текст: '{text}' - Мат найден?: {sf.regex_check(text)}")
        print(f"(ФазиВази) Текст: '{text}' - Нечеткое совпадение с матом?: {sf.fuzzy_check(text)}")
        print(f"(Робаст нейронка) Текст: '{text}' - Мат найден?: {sf.neural_check(text)}")
        print("\n")