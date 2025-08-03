from fastapi import FastAPI
from .orchestrator import RalexOrchestrator

app = FastAPI()
orchestrator = RalexOrchestrator()


@app.post("/voice-command")
async def process_voice_command(command: str, session_id: str):
    return await orchestrator.process_voice_command(command, session_id)


@app.get("/context/{session_id}")
async def get_session_context(session_id: str):
    return orchestrator.context_manager.get_context(session_id)


@app.post("/workflow/{workflow_name}")
async def execute_workflow(workflow_name: str, params: dict):
    return await orchestrator.execute_workflow(workflow_name, params)
