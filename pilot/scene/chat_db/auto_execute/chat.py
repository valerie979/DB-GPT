from pilot.scene.base_chat import BaseChat
from pilot.scene.base import ChatScene
from pilot.common.sql_database import Database
from pilot.configs.config import Config
from pilot.scene.chat_db.auto_execute.prompt import prompt

CFG = Config()


class ChatWithDbAutoExecute(BaseChat):
    chat_scene: str = ChatScene.ChatWithDbExecute.value()

    """Number of results to return from the query"""

    def __init__(self, chat_session_id, user_input, select_param: str = ""):
        chat_mode = ChatScene.ChatWithDbExecute
        self.db_name = select_param
        """ """
        super().__init__(
            chat_mode=chat_mode,
            chat_session_id=chat_session_id,
            current_user_input=user_input,
            select_param=self.db_name,
        )
        if not self.db_name:
            raise ValueError(
                f"{ChatScene.ChatWithDbExecute.value} mode should chose db!"
            )

        self.database = CFG.LOCAL_DB_MANAGE.get_connect(self.db_name)
        self.top_k: int = 200

    def generate_input_values(self):
        try:
            from pilot.summary.db_summary_client import DBSummaryClient
        except ImportError:
            raise ValueError("Could not import DBSummaryClient. ")
        client = DBSummaryClient()
        try:
            table_infos = client.get_db_summary(
                dbname=self.db_name,
                query=self.current_user_input,
                topk=CFG.KNOWLEDGE_SEARCH_TOP_SIZE,
            )
        except Exception as e:
            print("db summary find error!" + str(e))
            table_infos = self.database.table_simple_info()

        for info in table_infos:
            info['document'] = self.database.get_document_name(info['table'])

        input_values = {
            "input": self.current_user_input,
            "top_k": str(self.top_k),
            "dialect": self.database.dialect,
            "table_info": table_infos,
        }
        return input_values

    def do_action(self, prompt_response):
        print(f"do_action:{prompt_response}")
        return self.database.run(prompt_response.sql)