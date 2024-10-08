import requests
import json

from src.models.hugging_face.variables import eData, eCookies, eHeaders


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(eHeaders)
        self.session.cookies.update(eCookies)

    def create_dialogue(self):
        url = 'https://huggingface.co/chat/conversation'

        data = {"model": "meta-llama/Meta-Llama-3.1-70B-Instruct", "preprompt": "\n\n"}

        response = self.session.post(url, json=data)

        return response.json()

    def get_chats_data(self, conversation_id) -> dict[str | list[ str | dict[str | list]]]:
        self.session.headers['referer'] = "https://huggingface.co/chat/"
        "content-length" in self.session.headers and self.session.headers.pop("content-length")

        url = f'https://huggingface.co/chat/conversation/{conversation_id}/__data.json?x-sveltekit-invalidated=11'

        raw_data = self.session.get(url).json()

        return raw_data

    def get_initial_id(self, conversation_id):

        raw_data = self.get_chats_data(conversation_id)

        if "nodes" in raw_data:
            nodes = raw_data["nodes"]

            current_chat_node = nodes[1]["data"]

            initial_id = current_chat_node[3]

            return initial_id
        else:
            return ""

    def get_answer_from_title(self, conversation_id):
        raw_data = self.get_chats_data(conversation_id)

        if "nodes" in raw_data:
            nodes = raw_data["nodes"]

            current_chat_node = nodes[1]["data"]

            title_index = current_chat_node.index('title')+1

            answer_raw = current_chat_node[title_index]

            answer = answer_raw[1:]

            return answer

        return ""


    def send_message(self, conversation_id, message):
        url = f'https://huggingface.co/chat/conversation/{conversation_id}'

        initial_id = self.get_initial_id(conversation_id)

        self.session.headers['referer'] = url

        query = message.replace("'", '`').replace('"', "`").replace("\n", "").replace("\\", "/")
        data = (eData % (query, initial_id)).encode("utf-8")

        data_len = len(data) - 1

        self.session.headers["content-length"] = str(data_len)

        print(data)

        response = self.session.post(url, data, stream=True)

        raw_answer = response.content.decode().strip().split("\n")[-1]  # Known structure...

        answer = json.loads(raw_answer)['text']

        return answer

    def delete_dialogue(self, conversation_id):
        url = f'https://huggingface.co/chat/conversation/{conversation_id}'

        self.session.headers['referer'] = "https://huggingface.co/chat/"
        self.session.headers.pop("content-length")

        response = self.session.delete(url)

        return response.status_code
