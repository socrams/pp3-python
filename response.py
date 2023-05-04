from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

class Response:
    __tablename__="bot_response"

    id=Column(Integer, primary_key=True)
    answer=Column(String(500))
    response=Column(String(2000))
    options=Column(String(255))
    moreQuestion=Column(Boolean)
    moreOptions=Column(Boolean)

    def __init__(self, id, answer, response, options, moreQuestion, moreOptions) -> None:
        self.id = id
        self.answer=answer
        self.response=response
        self.options=options
        self.moreOptions=moreOptions
        self.moreQuestion=moreQuestion