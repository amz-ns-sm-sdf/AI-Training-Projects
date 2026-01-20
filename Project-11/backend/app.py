from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simulated agent tools
TOOLS = {
    'calculator': {
        'name': 'Calculator',
        'description': 'Performs mathematical calculations',
        'capability': 'Can add, subtract, multiply, divide'
    },
    'weather': {
        'name': 'Weather API',
        'description': 'Get weather information',
        'capability': 'Returns temperature, condition, humidity'
    },
    'web_search': {
        'name': 'Web Search',
        'description': 'Search the internet',
        'capability': 'Returns top search results'
    },
    'knowledge_base': {
        'name': 'Knowledge Base',
        'description': 'Query knowledge base',
        'capability': 'Returns information from documents'
    }
}

# Sample tool responses
TOOL_RESPONSES = {
    'calculator': lambda q: {
        'tool': 'calculator',
        'input': q,
        'output': '42',
        'reasoning': 'Interpreted as basic math operation'
    },
    'weather': lambda q: {
        'tool': 'weather',
        'input': q,
        'output': 'New York: 72°F, Sunny, Humidity 45%',
        'reasoning': 'Retrieved weather data'
    },
    'web_search': lambda q: {
        'tool': 'web_search',
        'input': q,
        'output': 'Top results: AI Trends 2024, Machine Learning Basics...',
        'reasoning': 'Searched the web'
    },
    'knowledge_base': lambda q: {
        'tool': 'knowledge_base',
        'input': q,
        'output': 'Found relevant documentation on agents and LLMs',
        'reasoning': 'Queried knowledge base'
    }
}

class Agent:
    """Simulated Langchain Agent"""
    def __init__(self, name):
        self.name = name
        self.tools = list(TOOLS.keys())
        self.memory = []
        self.thought_process = []
    
    def think(self, user_input):
        """Agent thinking process"""
        thoughts = [
            f"I received the input: '{user_input}'",
            "Let me break down what tools I might need...",
            "Analyzing the query for relevant tools...",
            "Determining the best approach..."
        ]
        return thoughts
    
    def select_tool(self, user_input):
        """Select appropriate tool"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['calculate', 'math', 'count', 'solve']):
            return 'calculator'
        elif any(word in user_lower for word in ['weather', 'temperature', 'rain']):
            return 'weather'
        elif any(word in user_lower for word in ['search', 'find', 'research', 'what is']):
            return 'web_search'
        else:
            return 'knowledge_base'
    
    def act(self, user_input):
        """Execute the agent"""
        # Think
        thoughts = self.think(user_input)
        self.thought_process = thoughts
        
        # Select tool
        selected_tool = self.select_tool(user_input)
        
        # Use tool
        tool_response = TOOL_RESPONSES[selected_tool](user_input)
        
        # Observe and return
        return {
            'agent_name': self.name,
            'user_input': user_input,
            'thought_process': thoughts,
            'tool_selected': selected_tool,
            'tool_response': tool_response,
            'final_answer': f"Based on {selected_tool}: {tool_response['output']}"
        }

# Create agent instance
agent = Agent("Alex")

@app.route('/api/agent-info', methods=['GET'])
def get_agent_info():
    """Get agent information"""
    return jsonify({
        "agent_name": agent.name,
        "available_tools": [
            {
                'id': k,
                'name': v['name'],
                'description': v['description'],
                'capability': v['capability']
            }
            for k, v in TOOLS.items()
        ],
        "model_type": "Langchain Agent Simulator",
        "memory_size": len(agent.memory)
    })

@app.route('/api/think', methods=['POST'])
def think():
    """Get agent thinking process"""
    try:
        data = request.json
        user_input = data.get('query', '')
        
        if not user_input:
            return jsonify({"error": "No query provided"}), 400
        
        thoughts = agent.think(user_input)
        selected_tool = agent.select_tool(user_input)
        
        return jsonify({
            "status": "success",
            "query": user_input,
            "thought_process": thoughts,
            "selected_tool": selected_tool,
            "tool_info": TOOLS[selected_tool]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/act', methods=['POST'])
def act():
    """Execute agent action"""
    try:
        data = request.json
        user_input = data.get('query', '')
        
        if not user_input:
            return jsonify({"error": "No query provided"}), 400
        
        # Add to memory
        agent.memory.append({
            'timestamp': datetime.now().isoformat(),
            'query': user_input
        })
        
        result = agent.act(user_input)
        
        return jsonify({
            "status": "success",
            "result": result,
            "memory_updated": len(agent.memory)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get agent memory"""
    return jsonify({
        "memory": agent.memory,
        "size": len(agent.memory),
        "last_updated": agent.memory[-1]['timestamp'] if agent.memory else None
    })

@app.route('/api/samples', methods=['GET'])
def get_samples():
    """Get sample queries"""
    return jsonify({
        "samples": [
            "Calculate 25 + 17",
            "What's the weather in New York",
            "Search for AI trends",
            "Tell me about machine learning agents",
            "How much is 100 * 5"
        ]
    })

if __name__ == '__main__':
    app.run(debug=False, port=5010, use_reloader=False)
