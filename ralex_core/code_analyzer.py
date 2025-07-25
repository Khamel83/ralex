import ast

class CodeAnalyzer:
    def __init__(self):
        pass

    def analyze(self, code: str) -> dict:
        try:
            tree = ast.parse(code)
            analysis = {
                "imports": [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)],
                "functions": [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
            }
            return analysis
        except SyntaxError as e:
            return {"error": str(e)}