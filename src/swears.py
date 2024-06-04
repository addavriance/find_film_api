import re
from fuzzywuzzy import fuzz
from check_swear import SwearingCheck


class SFilter:
    def __init__(self):
        self.sch = SwearingCheck()

        self.pattern = r"(?iu)\b(?:(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|(?:.\B)+?[оаеи-])-?)?(?:[её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|и[пб][ае][тцд][ьъ]).*?|(?:(?:н[иеа]|ра[зс]|[зд]?[ао](?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч)-?)?ху(?:[яйиеёю]|л+и(?!ган)).*?|бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|\S*?(?:п(?:[иеё]зд|ид[аое]?р|ед(?:р(?!о)|[аое]р|ик)|охую)|бля(?:[дбц]|тс)|[ое]ху[яйиеё]|хуйн).*?|(?:о[тб]?|про|на|вы)?м(?:анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]ь|ища)|уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|[ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й))|елд[ауые].*?|ля[тд]ь|(?:[нз]а|по)х)\b"

        self.pattern = re.compile(self.pattern, flags=re.I | re.U)

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

        if re.findall(self.pattern, cleared_text):
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

    ptexts = [
        ""
    ]

    for ptext in ptexts:
        print(f"(Регулярки) Текст: '{ptext}' - Мат найден?: {sf.regex_check(ptext)}")
        print(f"(ФазиВази) Текст: '{ptext}' - Нечеткое совпадение с матом?: {sf.fuzzy_check(ptext)}")
        print(f"(Робаст нейронка) Текст: '{ptext}' - Мат найден?: {sf.neural_check(ptext)}")
        print("\n")