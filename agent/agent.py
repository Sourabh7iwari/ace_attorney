from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from groq import Groq
from dotenv import load_dotenv
from agent.workflow import graph
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DebateRequest(BaseModel):
    topic: str
    metadata: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/debate")
async def start_debate(request: DebateRequest):
    try:
        if not request.topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
            
        # Create initial state
        from agent.state import create_initial_state
        initial_state = create_initial_state(request.topic)
        
        # Run the graph synchronously since LangGraph doesn't support async yet
        final_state = graph.invoke(initial_state)
        
        return {
            "topic": request.topic,
            "prosecutor_arguments": [arg.dict() for arg in final_state["prosecutor_arguments"]],
            "defendant_arguments": [arg.dict() for arg in final_state["defendant_arguments"]],
            "judgment": final_state.get("judgment"),
            "metadata": final_state["metadata"]
        }
        
    except Exception as e:
        print(f"Error in debate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/copilotkit")
async def copilotkit_handler(request: Request):
    try:
        data = await request.json()
        return {"message": "Request processed successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)