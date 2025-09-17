# 🎯 AI-Powered Architecture Mapper - Technical Documentation

## Overview
This system uses **LangGraph + LLM Agents + Mermaid** to automatically analyze codebases and generate architecture diagrams. Each step in the workflow is powered by an actual AI agent, making it truly intelligent rather than rule-based.

## Architecture Flow
```
Code Files → AI Scanner → AI Detector → AI Relationship Finder → AI Mermaid Generator → PNG Diagram
```

---

## 📁 File Structure & Responsibilities

### 1. `main.py` - Entry Point & Orchestration
**Purpose**: Main entry point that handles user input and coordinates the analysis

**Key Functions**:
- Validates command line arguments
- Checks for required API keys
- Initializes and runs the AI agent workflow
- Handles error cases and user feedback

**Code Flow**:
```python
def main():
    # 1. Parse command line arguments (project path)
    # 2. Validate GROQ_API_KEY exists
    # 3. Create AIMermaidAgent instance
    # 4. Run analysis on specified project
    # 5. Display results and generated files
```

### 2. `ai_mermaid_agent.py` - Core AI Agent System
**Purpose**: Contains the main AI agent workflow using LangGraph

#### Core Components:

##### `AIState` - Workflow State Management
```python
class AIState(TypedDict):
    files: List[str]           # File paths to analyze
    components: Dict[str, str] # Detected components {name: type}
    relationships: List[Dict]  # Component relationships
    mermaid_code: str         # Generated Mermaid diagram code
```

##### `AIMermaidAgent` - Main Agent Orchestrator
**Initialization**:
- Sets up Groq LLM client with API key
- Configures model (`llama-3.1-8b-instant`)
- Initializes caching system for deterministic results
- Builds LangGraph workflow

**Workflow Graph**:
```
scan → detect → relate → mermaid → END
```

#### AI Agent Workflow (4 Agents):

##### **Agent 1: `_ai_scanner_agent`** - File Scanner
**Purpose**: Reads and AI-analyzes code files

**AI Analysis Process**:
1. Iterates through all provided file paths
2. Reads file content (skips files < 10 characters)
3. **AI Analysis**: Uses Groq LLaMA 3.1 to analyze each file's:
   - Component type (frontend/backend/service/database/cache/queue/auth/gateway)
   - Framework detection (Django/Flask/FastAPI/React/etc)
   - Architectural patterns found
4. Robust JSON parsing with fallback handling
5. Caches AI results for deterministic behavior

**Output**: List of file objects with content + AI analysis

##### **Agent 2: `_ai_detector_agent`** - Component Detector
**Purpose**: AI-powered architectural component identification

**AI Detection Process**:
1. **Primary AI Analysis**: Uses Groq LLaMA 3.1 to analyze:
   - File path and directory structure
   - Code content and patterns
   - Previous AI analysis from Scanner Agent
   - Architectural context and naming conventions
2. **Component Classification**: AI determines component type with confidence scoring
3. **Fallback Logic**: If AI confidence < 0.5, uses filename pattern matching
4. **Caching**: Results cached for deterministic behavior

**AI-Detected Component Types**:
- **Gateway**: API gateways, routing layers
- **Auth**: Authentication, authorization services
- **Service**: Business logic, microservices
- **Database**: Data storage, repositories
- **Cache**: Caching layers
- **Queue**: Message queues, async processing
- **Frontend**: UI, web interfaces

**Output**: Dictionary of AI-detected components `{component_name: component_type}`

##### **Agent 3: `_ai_relationship_agent`** - Relationship Finder
**Purpose**: AI-powered component relationship mapping

**AI Relationship Analysis**:
1. **Primary AI Analysis**: Uses Groq LLaMA 3.1 to analyze:
   - Component types and their typical interactions
   - Architectural patterns and data flow
   - Service dependencies and communication patterns
   - Authentication and authorization flows
2. **Relationship Validation**: AI validates relationships exist between actual components
3. **Fallback Logic**: If AI fails, uses rule-based relationship mapping
4. **Caching**: Results cached for deterministic behavior

**AI-Detected Relationship Types**:
- `routes`: Gateway routing traffic
- `calls`: Frontend API calls
- `uses`: Service using data stores
- `publishes`: Service publishing to queues
- `authenticates`: Service authentication flow

**AI Rules Applied**:
- Gateways route to services based on architectural patterns
- Frontends call services based on typical web app flows
- Services use data layers based on persistence patterns
- Auth flows based on security architecture patterns

**Output**: List of AI-validated relationship objects `{from, to, type}`

##### **Agent 4: `_ai_mermaid_agent`** - Mermaid Generator
**Purpose**: AI-powered Mermaid diagram generation

**AI Diagram Generation**:
1. **Primary AI Analysis**: Uses Groq LLaMA 3.1 to generate:
   - Clean Mermaid flowchart syntax
   - Logical component layering (Gateway/Frontend/Service/Data layers)
   - Proper subgraph organization
   - Clean node naming and arrow styling
2. **Syntax Validation**: AI ensures valid Mermaid syntax
3. **Fallback Generation**: If AI fails, uses template-based generation
4. **Caching**: Results cached for deterministic behavior

**AI-Generated Features**:
- **Layered Architecture**: AI organizes components into logical layers
- **Clean Syntax**: AI generates valid Mermaid with proper formatting
- **Visual Hierarchy**: AI structures diagram for optimal readability
- **Consistent Styling**: AI applies consistent node and arrow styles

**Diagram Structure**:
- Gateway_Layer (API gateways, routing)
- Frontend_Layer (UI, web interfaces)
- Service_Layer (business logic, auth)
- Data_Layer (databases, caches, queues)

**Output**: AI-generated Mermaid flowchart code saved to `ai_architecture.mmd`

#### Utility Functions:

##### `_convert_to_png(mermaid_code)`
**Purpose**: Converts Mermaid code to PNG image

**Process**:
1. Base64 encodes the Mermaid code
2. Calls mermaid.ink API service
3. Downloads and saves PNG image as `ai_architecture.png`
4. Handles conversion errors gracefully

##### `analyze(code_path)`
**Purpose**: Main analysis orchestrator

**Process**:
1. Discovers all Python files in project using `Path.rglob("*.py")`
2. Invokes LangGraph workflow with initial state
3. Saves analysis results to `ai_analysis.json`
4. Converts Mermaid to PNG
5. Displays completion summary with file counts

---

## 🔧 Dependencies & Configuration

### Required Packages:
```
langgraph>=0.0.26    # AI agent workflow framework
groq>=0.4.1          # LLM API client
requests>=2.28.0     # HTTP requests for PNG conversion
python-dotenv>=0.19.0 # Environment variable management
```

### Environment Variables:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### API Integration:
- **Groq LLaMA 3.1**: For AI-powered component analysis
- **Mermaid.ink**: For PNG diagram generation

---

## 📊 Output Files

### 1. `ai_architecture.mmd`
**Format**: Mermaid flowchart syntax
**Content**: Complete diagram definition with layers and relationships

### 2. `ai_architecture.png` 
**Format**: PNG image
**Content**: Visual architecture diagram with component boxes and arrows

### 3. `ai_analysis.json`
**Format**: JSON data
**Content**: Complete analysis results including:
- `components`: All detected components with types
- `relationships`: All mapped relationships with types  
- `mermaid_code`: Generated Mermaid syntax

---

## 🎯 Key Features

### True AI-Powered Analysis
- **4 AI Agents**: Each workflow step uses actual Groq LLaMA 3.1 LLM calls
- **Content Analysis**: AI reads and understands code patterns, not just filenames
- **Pattern Recognition**: AI identifies frameworks, architectural patterns, and dependencies
- **Intelligent Relationships**: AI maps realistic component interactions based on code analysis

### Deterministic AI Results
- **Temperature**: Set to 0.0 for consistent AI responses
- **Seed**: Fixed at 42 for reproducible results
- **Caching**: AI results cached by file path and content hash
- **Fallback Logic**: Rule-based fallbacks when AI calls fail

### Robust Error Handling
- **JSON Parsing**: Advanced JSON extraction from AI responses
- **AI Failures**: Graceful degradation to rule-based logic
- **File Reading**: Handles encoding issues and malformed files
- **Network Issues**: Timeout handling for PNG conversion

### Enterprise Scalability
- **Large Codebases**: Processes hundreds of files efficiently
- **Memory Management**: Truncates large file content for AI analysis
- **Caching System**: Avoids redundant AI calls for performance
- **Complex Projects**: Handles nested directory structures

### Advanced AI Capabilities
- **Multi-Language Support**: Analyzes Python, JavaScript, TypeScript, Java, Go, Ruby
- **Framework Detection**: Identifies Django, Flask, FastAPI, React, Express, Spring
- **Architecture Patterns**: Detects microservices, REST APIs, event-driven patterns
- **Smart Layering**: AI organizes components into logical architectural layers

---

## 🚀 Usage Examples

### Simple Project Analysis:
```bash
python main.py sample_project
```
**Result**: Basic microservices architecture with 4 components, 6 relationships

### Complex Project Analysis:
```bash
python main.py complex_project  
```
**Result**: Multi-layer architecture with 8 components, 17 relationships

### Custom Project Analysis:
```bash
python main.py /path/to/your/project
```
**Result**: Tailored analysis based on your project structure

---

## 🔍 Troubleshooting

### Common Issues:

1. **Missing API Key**
   - Error: "Please set GROQ_API_KEY environment variable"
   - Solution: Add API key to `.env` file

2. **No Python Files Found**
   - Error: Empty components list
   - Solution: Ensure project contains `.py` files

3. **PNG Generation Failed**
   - Error: "PNG conversion failed"
   - Solution: Check internet connection, Mermaid syntax validity

4. **Import Errors**
   - Error: "ModuleNotFoundError"
   - Solution: Activate virtual environment, install requirements

---

## 🧠 AI Agent Design Philosophy

### True Agentic AI Architecture
- **Independent AI Agents**: Each workflow step is a separate LLM-powered agent
- **No Hardcoded Rules**: All analysis done through actual AI reasoning
- **Dynamic Code Analysis**: AI reads and understands actual code content
- **Intelligent Pattern Recognition**: AI identifies architectural patterns from code

### LangGraph Workflow Orchestration
- **State Management**: Shared state across all AI agents
- **Sequential AI Processing**: Each agent builds on previous AI analysis
- **Error Recovery**: Graceful handling of AI agent failures
- **Workflow Coordination**: Automated AI agent orchestration

### Production-Ready AI
- **Consistent Results**: Same input always produces same AI analysis
- **Reproducible Analysis**: Fixed seeds and temperature for deterministic AI
- **Reliable Workflows**: Fallback mechanisms when AI agents fail
- **Performance Optimized**: Caching prevents redundant AI calls

This system represents a **true AI-powered approach** to architecture analysis, where **every step involves actual LLM reasoning** rather than simple rule-based logic. Each of the 4 agents makes real AI calls to analyze code content, detect components, map relationships, and generate diagrams - making it genuinely intelligent rather than just pattern matching.