# AI Training Projects Demo Guide

## Complete Project Suite (Projects 1-14)

All projects are now set up and ready to run. Here's the complete guide with demo prompts and expected outputs.

---

## Project Setup Information

| Project | Description | Backend Port | Frontend Port | Focus Area |
|---------|-------------|--------------|---------------|-----------|
| 1 | Simple Chatbot | 5000 | 3000 | Basic LLM Chat |
| 2 | Login & History | 5001 | 3001 | User Auth |
| 3 | Thread Management | 5002 | 3002 | Conversation Threads |
| 4 | Memory Context | 5003 | 3003 | Conversation Memory |
| 5 | Rich Media | 5004 | 3004 | Markdown, Code, Formulas |
| 6 | Image Generation | 5005 | 3005 | Image Synthesis |
| 7 | RAG Document Chat | 5006 | 3005 | Document Q&A |
| 8 | Database Q&A | 5007 | 3006 | SQL from NL |
| 9 | Excel/Sheet Q&A | 5008 | 3007 | Spreadsheet Analytics |
| 10 | Image Rules Validator | 5009 | 3008 | Computer Vision Rules |
| 11 | Langchain Agent | 5010 | 3009 | Agent Reasoning |
| 12 | Tic Tac Toe Agent | 5011 | 3010 | Game Playing Agent |
| 13 | MCP Agent | 5012 | 3011 | Protocol Standards |
| 14 | N8N Workflow | 5013 | 3012 | Automation Workflows |

---

## PROJECT 1: Simple Chatbot
**URL:** http://localhost:3000

### Demo Prompts:
- "Hello, how are you?"
- "What can you do?"
- "Tell me about AI"

### Expected Outputs:
```
User: Hello, how are you?
Bot: Hello! I'm doing well, thanks for asking. How can I help you today?

User: Tell me about AI
Bot: Artificial Intelligence is a fascinating field that encompasses machine learning, 
deep learning, and natural language processing. AI systems can process large amounts 
of data and learn patterns to make intelligent decisions.
```

---

## PROJECT 2: Login & Chat History
**URL:** http://localhost:3001

### Demo Flow:
1. Login with email: `user@example.com`
2. Type message: "What is machine learning?"

### Expected Output:
```
Login Screen → Chat History Display
Shows previous conversations for the logged-in user
Chat History Panel displays: "What is machine learning?" 
Bot Response: "Machine learning is a subset of AI..."
```

---

## PROJECT 3: Thread Management
**URL:** http://localhost:3002

### Demo Prompts:
1. Click "+ New Thread" 
2. Type: "Explain neural networks"
3. Switch threads in sidebar
4. Type: "What about transformers?"

### Expected Features:
- Sidebar with thread list
- Thread creation/deletion
- Thread switching with conversation isolation
- Active thread highlighting

---

## PROJECT 4: Memory Context
**URL:** http://localhost:3003

### Demo Conversation:
1. "My name is Alice"
2. "I like AI"
3. "What did I say about my interests?"

### Expected Output:
```
Message 3 Response:
"[Context aware] Considering previous messages (2/5 in memory):
You mentioned that you like AI. This is relevant to your current query."

Memory Indicator: [███ 3/5]
```

---

## PROJECT 5: Rich Media Support
**URL:** http://localhost:3004

### Demo Prompts:
- "Show code example"
- "Display a formula"
- "Create a table"
- "Embed an image"

### Expected Output:
```markdown
## Python Function Example

```python
def hello_world():
    print("Hello, World!")
```

## Mathematical Formula
$f(x) = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

| Language | Use Case |
|----------|----------|
| Python | Data Science |
| JavaScript | Web Dev |
```

---

## PROJECT 6: Image Generation
**URL:** http://localhost:3005

### Demo Prompts:
- "Generate image of sunset"
- "Create mountain landscape"
- "Show ocean waves"
- "Generate abstract art"

### Expected Output:
```
User: Generate image of sunset
Bot: 🖼️ Generated Image
[Image with sunset theme displayed]
Prompt: sunset
Model: Gemini 2.0 Simulation
Timestamp: 2026-01-20 20:30:45
```

---

## PROJECT 7: RAG Document Chat
**URL:** http://localhost:3005

### Demo Flow:
1. Click "Load Samples"
2. Select "AI Fundamentals"
3. Ask: "What is machine learning?"

### Expected Output:
```
Query: What is machine learning?
Retrieved Chunks: 2
Response: Based on AI Fundamentals:
"Machine Learning enables systems to learn from data. 
Deep Learning uses neural networks with multiple layers..."
```

---

## PROJECT 8: Database Q&A
**URL:** http://localhost:3006

### Demo Prompts:
- "Show all customers"
- "List customers from USA"
- "What is total revenue?"
- "High value orders"

### Expected Output:
```
SQL Generated: SELECT * FROM customers WHERE country = "USA";

Results:
| ID | Name | Email | Country |
|----|------|-------|---------|
| 1 | Alice | alice@co.com | USA |
| 4 | David | david@co.com | USA |

✓ Returned 2 row(s)
```

---

## PROJECT 9: Excel/Sheet Q&A
**URL:** http://localhost:3007

### Demo Prompts:
- "Show north region sales"
- "What is total revenue?"
- "Engineering department employees"

### Expected Output:
```
Sheet: Sales
Query: Show north region sales

Results:
| Month | Product | Quantity | Revenue | Region |
|-------|---------|----------|---------|--------|
| Jan | Laptop | 150 | 180000 | North |
| Feb | Laptop | 180 | 216000 | North |
| Mar | Laptop | 200 | 240000 | North |
```

---

## PROJECT 10: Image Rules Validator
**URL:** http://localhost:3008

### Demo Flow:
1. Select Rule Set: "Product Photo"
2. Click a Sample Image
3. View Validation Results

### Expected Output:
```
Validation Score: 80%

✓ High quality and clear visibility
✓ Product must be centered
✗ No text or watermarks
✓ Square format (1:1 ratio)

Recommendation: Image approved
```

---

## PROJECT 11: Langchain Agent
**URL:** http://localhost:3009

### Demo Prompts:
- "Calculate 25 + 17"
- "What's the weather in New York?"
- "Search for AI trends"

### Expected Output:
```
Agent Thinking Process:
→ I received the input: 'Calculate 25 + 17'
→ Let me break down what tools I might need...
→ Analyzing the query for relevant tools...
→ Determining the best approach...

Tool Selected: calculator
Input: Calculate 25 + 17
Output: 42

✓ Based on calculator: 42
```

---

## PROJECT 12: Tic Tac Toe Agent
**URL:** http://localhost:3010

### Demo Play:
1. Click center cell (position 4)
2. Agent plays automatically
3. Continue playing to win or lose
4. Click "New Game" to restart

### Expected Features:
- Real-time agent moves
- Move log with positions
- Win/Loss/Draw detection
- Smart agent strategy

---

## PROJECT 13: MCP Agent
**URL:** http://localhost:3011

### Demo Flow:
1. Select Service: "Text Processor"
2. Enter payload: "Hello MCP Protocol"
3. Click Send Request
4. View JSON Response

### Expected Output:
```json
{
  "status": "success",
  "request": {
    "service": "text_processor",
    "payload": "Hello MCP Protocol"
  },
  "response": {
    "service": "text_processor",
    "result": {
      "word_count": 3,
      "char_count": 17,
      "analysis": "Text processed via MCP"
    }
  },
  "protocol": "MCP v1.0"
}
```

---

## PROJECT 14: N8N Workflow Automation
**URL:** http://localhost:3012

### Demo Flow:
1. Select Workflow: "Email Notification"
2. Click "Execute Workflow"
3. View Execution History

### Expected Output:
```
Execution History:
✓ SUCCESS - Email Notification - 1.2s
  Records Processed: 42
  
✓ SUCCESS - Data Sync - 2.5s
  Records Processed: 156

✓ SUCCESS - Slack Alert - 0.8s
  Records Processed: 12
```

---

## Running All Projects

### Start All Services:
```bash
# Start all backends (run in separate terminals)
cd Project-8/backend && python app.py   # port 5007
cd Project-9/backend && python app.py   # port 5008
cd Project-10/backend && python app.py  # port 5009
cd Project-11/backend && python app.py  # port 5010
cd Project-12/backend && python app.py  # port 5011
cd Project-13/backend && python app.py  # port 5012
cd Project-14/backend && python app.py  # port 5013

# Start all frontends (run in separate terminals)
cd Project-8/frontend && python server.py   # port 3006
cd Project-9/frontend && python server.py   # port 3007
cd Project-10/frontend && python server.py  # port 3008
cd Project-11/frontend && python server.py  # port 3009
cd Project-12/frontend && python server.py  # port 3010
cd Project-13/frontend && python server.py  # port 3011
cd Project-14/frontend && python server.py  # port 3012
```

---

## Key Features Overview

### Database Projects (8-9)
- Natural Language to SQL/Query conversion
- Mock database with customers and orders
- Spreadsheet analytics with multiple sheets
- Sample queries for quick testing

### Vision Projects (10)
- Image validation against rule sets
- Simulated computer vision checks
- Score-based approval system
- Multiple rule set templates

### Agent Projects (11-14)
- **Project 11**: Shows agent thinking process, tool selection, and execution
- **Project 12**: Game-playing agent with strategic moves
- **Project 13**: Protocol-based inter-service communication (MCP)
- **Project 14**: Workflow automation with execution tracking

---

## Testing Checklist

- [ ] All 14 projects created with folders
- [ ] All backends running on ports 5007-5013
- [ ] All frontends running on ports 3006-3012
- [ ] Demo prompts tested for each project
- [ ] Expected outputs match actual outputs
- [ ] All features (tables, charts, validations) working
- [ ] Agent reasoning visible in project 11
- [ ] Game mechanics working in project 12
- [ ] Protocol handling in project 13
- [ ] Workflow execution in project 14

---

## Notes

- All projects use in-memory storage (no database required)
- Mock data simulates real API responses
- Agent implementations are simplified for demo purposes
- Focus is on UI/UX and feature demonstration
- Each project can be extended with real APIs and databases
