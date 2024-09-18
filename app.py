from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# Import your LangChain logic (if it’s in a separate file)
from rag_chain import conversational_rag_chain, get_session_history

os.environ['USER_AGENT'] = 'MyLangChainApp/1.0'

# Define the FastAPI app
app = FastAPI()

# Pydantic model to validate the request body
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
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))