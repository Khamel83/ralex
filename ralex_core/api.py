from fastapi import FastAPI
from .v4_orchestrator import RalexV4Orchestrator

app = FastAPI()
orchestrator = RalexOrchestrator()

@app.post("/v4/voice-command")
async def process_voice_command(command: str, session_id: str):
    return await orchestrator.process_voice_command(command, session_id)

@app.get("/v4/context/{session_id}")
async def get_session_context(session_id: str):
    return orchestrator.context_manager.get_context(session_id)

@app.post("/v4/workflow/{workflow_name}")
async def execute_workflow(workflow_name: str, params: dict):
    return await orchestrator.execute_workflow(workflow_name, params)