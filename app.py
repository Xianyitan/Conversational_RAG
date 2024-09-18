from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from rag_chain import conversational_rag_chain, get_session_history

os.environ['USER_AGENT'] = 'MyLangChainApp/1.0'

# Define the FastAPI app
app = FastAPI()

class QueryInput(BaseModel):
    session_id: str
    input: str

@app.post("/ask")
async def ask_question(query: QueryInput):
    try:
        # Get chat history
        session_id = query.session_id
        chat_input = query.input

        # Retrieve or create the chat history for this session
        session_history = get_session_history(session_id)

        # Invoke the RAG chain to get the answer
        result = conversational_rag_chain.invoke(
            {"input": chat_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Return the answer in JSON format
        return {"answer": result["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))