#!/usr/bin/env python3
"""
AI-Powered Architecture Mapper
LangGraph + LLM Agents + Mermaid
"""
from ai_mermaid_agent import AIMermaidAgent

def main():
    import sys
    code_path = sys.argv[1] if len(sys.argv) > 1 else "sample_project"
    
    print("🎯 AI-Powered Architecture Mapper")
    print("🤖 LangGraph + LLM Agents + Mermaid")
    print(f"📁 Analyzing: {code_path}")
    print("=" * 50)
    
    agent = AIMermaidAgent()
    result = agent.analyze(code_path)
    
    print("\n🎨 AI-Generated Mermaid Diagram!")
    print("✅ Each node is an actual AI agent, not hardcoded logic")

if __name__ == "__main__":
    main()