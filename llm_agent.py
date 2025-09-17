#!/usr/bin/env python3
import json
import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class LLMAgent:
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        
    def analyze_code(self, file_path, content):
        """Use LLM to analyze code and detect components"""
        prompt = f"""
Analyze this code file and identify architectural components. Return JSON only.

File: {file_path}
Code:
```
{content[:2000]}  # Limit context
```

Detect these component types with confidence (0.0-1.0):
- microservice
- api_gateway  
- database
- message_queue
- auth_service
- cache

Return JSON format:
{{
  "components": [
    {{
      "name": "component_name",
      "type": "component_type", 
      "confidence": 0.85,
      "reasoning": "why detected"
    }}
  ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.1,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            # Extract JSON from response
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(result[start:end])
            return {"components": []}
            
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return {"components": []}
    
    def detect_relationships(self, components):
        """Use LLM to detect relationships between components"""
        prompt = f"""
Given these components, identify relationships between them. Return JSON only.

Components:
{json.dumps(components, indent=2)}

Return relationships in format:
{{
  "relationships": [
    {{
      "from": "component1",
      "to": "component2", 
      "type": "relationship_type",
      "reasoning": "why connected"
    }}
  ]
}}

Common relationship types: uses, routes_to, publishes_to, authenticates, caches
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.1,
                max_tokens=800
            )
            
            result = response.choices[0].message.content
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(result[start:end])
            return {"relationships": []}
            
        except Exception as e:
            print(f"Relationship detection failed: {e}")
            return {"relationships": []}
    
    def chat_about_architecture(self, query, current_components, context=""):
        """Chat interface for architecture questions and updates"""
        prompt = f"""
You are an architecture expert. Answer questions about the current system architecture.

Current Architecture:
{json.dumps(current_components, indent=2)}

Context: {context}

User Question: {query}

If the user wants to modify the architecture, return JSON with "action" and "changes".
Otherwise, provide a helpful explanation.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Chat failed: {e}"