COUNTRIES = ['RU', 'UA', 'BY', 'KZ', 'CN', 'TW', 'HK', "JP", 'PT', 'BR']

messages = {
        'ru': f"""
        Ты в роли специалиста по фильмам, гениального поисковика фильмов и тебе был задан такой запрос/описание,
        по которому ты должен понять какой фильм описан, это может быть отрывок из фильма или ситуация,
        или что то схожее, даже без жанра и остального, только описание могут написать.

        Ты должен дать ответ в формате json, сырой json без блоков кода и остального. Ответ начинается и заканчивается фигурными скобками {{}}.

        Твой ответ строго содержит поля:
        "fn" - название фильма
        "fd" - дата выхода фильма, сторого просто год, иначе null,

        Итак, запрос пользователя на поиск фильма: %s

        Если запрос ругательный, ответь одной цифрой кода ответа без json.
        
        0 - Фильм не найден.
        1 - Запрос ругательный/оскорбительный.
        """,

        'en': f"""
        You're in the role of movie expert, genius movie finder and you've been given this query/description,
        and you have to figure out what movie it's describing, it could be an excerpt from a movie or a situation,
        or something similar, even without genre or anything else, just a description.

        You have to give the answer in json format, raw json without code blocks and stuff. The answer starts and ends with curly braces {{}}.

        Your answer strictly contains the fields:
        "fn" - the title of the movie
        "fd" - the release date of the movie, strictly just the year, otherwise null,

        Otherwise, if there is no answer/movie, or the query is not appropriate or does not match the movie search, return/answer the required return code, no json, just the code, one digit.
        Meaning of return codes:

        0 - Movie not found.
        1 - The query is unacceptable or does not contain a movie search.
        2 - The query contains little data.

        So, the user's request to search for a movie is: %s

        If the query is abusive, reply with a one digit response code without json.
        """,

        'zh': f"""
        你的角色是一名电影专家，一名出色的电影搜索者、
        你必须找出它描述的是哪部电影，它可以是一部电影的节选，也可以是一个场景、
        或类似的东西，甚至不需要类型或其他任何东西，只需要一个描述。

        你必须以 json 格式给出答案，原始的 json 格式，不含代码块之类的东西。答案以大括号 {{}} 开始和结束。

        您的答案必须包含以下字段
        "fn"（电影名）--根据查询的语言提供的电影名称。
        "fd" - 电影上映日期，严格来说只有年份，否则为空、

        否则，如果没有答案/电影，或者查询不合适或与电影搜索不匹配，则返回/回答所需的返回代码，没有 json，只有代码，一位数。
        返回代码的含义：

        0 - 未找到影片。
        1 - 查询不可接受或不包含影片搜索。
        2 - 查询包含的数据很少。

        因此，用户搜索电影的请求是：%s

        如果查询是滥用的，则回复一个不含 json 的一位数响应代码。
        """,

        'ja': f"""
        あなたは映画の専門家であり、優れた映画検索エンジンの役割を担っている、
        それがどんな映画なのか、映画の抜粋かもしれないし、シチュエーションかもしれない、
        映画の抜粋でもいいし、シチュエーションでもいい。

        答えはjson形式で、コードブロックなどを含まない生のjsonで与えなければならない。答えは中括弧{{}}で始まり、{{}}で終わります。

        回答には以下のフィールドが含まれます：
        "fn"-クエリの言語で指定された映画のタイトル。
        "fd"-映画の公開日、厳密には年、そうでなければnull、

        それ以外の場合、答え/映画がない場合、クエリが適切でない場合、または映画検索にマッチしない場合、必要なリターンコードを返す/答える。
        リターンコードの意味

        0 - 映画が見つかりません。
        1 - クエリが受け付けられないか、映画検索を含んでいない。
        2 - クエリに含まれるデータが少ない。

        つまり、ユーザーの映画検索リクエストは %s です。

        クエリが不正な場合は、jsonなしで1桁のレスポンス・コードを返します。
        """,

        'pt': f"""
        Estás no papel de um perito em cinema, um brilhante descobridor de filmes e foi-te dada uma pergunta/descrição,
        que tens de descobrir que filme está a descrever, pode ser um excerto de um filme ou uma situação,
        ou algo semelhante, mesmo sem género ou qualquer outra coisa, apenas uma descrição.

        Tens de dar a resposta em formato json, json em bruto, sem blocos de código e outras coisas. A resposta começa e termina com chavetas {{}}.

        A tua resposta contém estritamente os campos:
        "fn" - o título do filme, dado o idioma da consulta.
        "fd" - a data de lançamento do filme, estritamente apenas o ano; caso contrário, nulo,

        Caso contrário, se não houver resposta/filme, ou se a consulta não for adequada ou não corresponder à pesquisa de filmes, devolve/responde o código de devolução requerido, sem json, apenas o código, um dígito.
        Significado dos códigos de retorno:

        0 - Filme não encontrado.
        1 - A consulta não é aceitável ou não contém uma pesquisa de filmes.
        2 - A consulta contém poucos dados.

        Assim, o pedido do utilizador para procurar um filme é: %s

        Se a consulta for abusiva, responder com um código de resposta de um dígito sem json.
        """
    }


def get_prompt(query: str, country: str) -> str:

    language = 'en'

    if country in COUNTRIES:
        if country in ['RU', 'UA', 'BY', 'KZ']:
            language = 'ru'
        elif country in ['CN', 'TW', 'HK']:
            language = 'zh'
        elif country in ['JP']:
            language = 'ja'
        elif country in ['PT', 'BR']:
            language = 'pt'

    message = messages[language] % query

    return message


MAX_QUERY_LEN = 250

MIN_QUERY_LEN = 10
