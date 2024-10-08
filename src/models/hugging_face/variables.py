url = 'https://huggingface.co/chat/conversation/'

eHeaders = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
    "cache-control": "no-cache",
    "content-type": "multipart/form-data; boundary=----0",
    "origin": "https://huggingface.co",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://huggingface.co/chat/",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

eCookies = {}  # Hidden

eData = '------0\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{\"inputs\":\"%s\",\"id\":\"%s\",\"is_retry\":false,\"is_continue\":false,\"web_search\":false,\"tools\":[]}\r\n------0--\r\n'
