import json
from datetime import datetime
import os

from .project_status_assessment import ProjectStatusAssessment

class DailyBriefingGenerator:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.assessor = ProjectStatusAssessment(project_root)

    def generate_briefing(self) -> str:
        status = self.assessor.assess_status()

        briefing = f"Daily Project Briefing ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
        briefing += "=========================================\n\n"

        briefing += "Project Overview:\n"
        briefing += f"  - Last Assessment: {status.get('last_assessment', 'N/A')}\n"
        briefing += f"  - Python Files: {status.get('python_file_count', 'N/A')}\n"
        briefing += f"  - Last Git Commit: {status.get('last_git_commit', 'N/A')}\n"
        briefing += "\n"

        briefing += "Key Metrics (Placeholder):\n"
        briefing += "  - No new metrics available yet. (Implement more assessments in ProjectStatusAssessment)\n"
        briefing += "\n"

        briefing += "Actionable Insights (Placeholder):\n"
        briefing += "  - No actionable insights generated yet. (Implement logic for insights)\n"
        briefing += "\n"

        briefing += "Next Steps (Placeholder):\n"
        briefing += "  - Continue with planned tasks.\n"

        return briefing

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    briefing_generator = DailyBriefingGenerator(project_root)
    briefing = briefing_generator.generate_briefing()
    print(briefing)
