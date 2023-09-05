from pilot.scene.base_chat import BaseChat
from pilot.common.sql_database import Database
from pilot.configs.config import Config

CFG = Config()

class ChatPipeline(BaseChat):
    def __init__(self, chat_session_id, user_input, select_param: str = ""):
        super().__init__(
            chat_mode=ChatScene.ChatWithDbExecute,
            chat_session_id=chat_session_id,
            current_user_input=user_input,
            select_param=select_param,
        )
        self.database = CFG.LOCAL_DB_MANAGE.get_connect(self.db_name)

    def handle_user_input(self, user_input):
        # TODO: Implement method to handle user_input

    def generate_response(self):
        # TODO: Implement method to generate response

    def maintain_chat_state(self):
        # TODO: Implement method to maintain chat state