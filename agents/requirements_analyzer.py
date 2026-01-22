"""Requirements Analyzer Agent using Google ADK"""
import json
from typing import Dict, Any
from google import genai
from google.genai import types
import config
from context.models import RequirementSpec


class RequirementsAnalyzer:
    """Agent that analyzes problem statements and generates requirements"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = config.MODEL_NAME
    
    async def analyze(self, problem_statement: str) -> RequirementSpec:
        """
        Analyze a problem statement and return structured requirements
        """
        prompt = f"""{config.REQUIREMENTS_ANALYZER_PROMPT}

Problem Statement:
{problem_statement}

Please analyze this and provide:
1. List of functional components needed
2. Recommended tech stack (frontend and backend)
3. Any clarifications needed (if requirements are unclear)
4. Complexity assessment (simple/medium/complex)

Respond in JSON format:
{{
    "functional_components": ["component1", "component2", ...],
    "tech_stack": {{"frontend": "React", "backend": "Flask"}},
    "clarifications": ["question1", "question2", ...] or null,
    "complexity": "simple"
}}
"""
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            return RequirementSpec(
                functional_components=result.get("functional_components", []),
                tech_stack=result.get("tech_stack", {"frontend": "React", "backend": "Flask"}),
                clarifications=result.get("clarifications"),
                complexity=result.get("complexity", "simple")
            )
            
        except Exception as e:
            print(f"Error in requirements analysis: {e}")
            # Return default requirements on error
            return RequirementSpec(
                functional_components=["Basic UI", "Core functionality"],
                tech_stack={"frontend": "React", "backend": "Flask"},
                complexity="simple"
            )
    
    def sync_analyze(self, problem_statement: str) -> RequirementSpec:
        """Synchronous version of analyze"""
        prompt = f"""{config.REQUIREMENTS_ANALYZER_PROMPT}

Problem Statement:
{problem_statement}

Please analyze this and provide:
1. List of functional components needed
2. Recommended tech stack (frontend and backend)
3. Any clarifications needed (if requirements are unclear)
4. Complexity assessment (simple/medium/complex)

Respond in JSON format:
{{
    "functional_components": ["component1", "component2", ...],
    "tech_stack": {{"frontend": "React", "backend": "Flask"}},
    "clarifications": ["question1", "question2", ...] or null,
    "complexity": "simple"
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            return RequirementSpec(
                functional_components=result.get("functional_components", []),
                tech_stack=result.get("tech_stack", {"frontend": "React", "backend": "Flask"}),
                clarifications=result.get("clarifications"),
                complexity=result.get("complexity", "simple")
            )
            
        except Exception as e:
            print(f"Error in requirements analysis: {e}")
            return RequirementSpec(
                functional_components=["Basic UI", "Core functionality"],
                tech_stack={"frontend": "React", "backend": "Flask"},
                complexity="simple"
            )
