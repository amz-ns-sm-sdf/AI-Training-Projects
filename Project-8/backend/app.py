from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Mock database - simulating different tables
MOCK_DATABASE = {
    'customers': [
        {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@company.com', 'country': 'USA', 'signup_date': '2024-01-15'},
        {'id': 2, 'name': 'Bob Smith', 'email': 'bob@company.com', 'country': 'UK', 'signup_date': '2024-02-20'},
        {'id': 3, 'name': 'Carol White', 'email': 'carol@company.com', 'country': 'Canada', 'signup_date': '2024-03-10'},
        {'id': 4, 'name': 'David Brown', 'email': 'david@company.com', 'country': 'USA', 'signup_date': '2024-01-25'},
    ],
    'orders': [
        {'id': 101, 'customer_id': 1, 'product': 'Laptop', 'amount': 1200, 'date': '2024-06-01', 'status': 'delivered'},
        {'id': 102, 'customer_id': 2, 'product': 'Mouse', 'amount': 25, 'date': '2024-06-05', 'status': 'delivered'},
        {'id': 103, 'customer_id': 1, 'product': 'Keyboard', 'amount': 75, 'date': '2024-06-10', 'status': 'pending'},
        {'id': 104, 'customer_id': 3, 'product': 'Monitor', 'amount': 300, 'date': '2024-06-15', 'status': 'delivered'},
    ]
}

# Sample queries mapping
QUERY_SAMPLES = {
    'all_customers': {'table': 'customers', 'description': 'Get all customers'},
    'usa_customers': {'table': 'customers', 'filter': 'country = USA', 'description': 'Get customers from USA'},
    'total_orders': {'table': 'orders', 'aggregate': 'count', 'description': 'Total number of orders'},
    'high_value_orders': {'table': 'orders', 'filter': 'amount > 100', 'description': 'Orders over $100'},
    'customer_orders': {'table': 'orders', 'join': 'customers', 'description': 'Orders with customer details'},
}

def process_natural_language_query(query_text):
    """Simulate NL to SQL conversion and query execution"""
    query_lower = query_text.lower()
    
    # Keyword matching for different query types
    if 'customer' in query_lower and ('all' in query_lower or 'list' in query_lower):
        return {
            'sql': 'SELECT * FROM customers;',
            'results': MOCK_DATABASE['customers'],
            'row_count': len(MOCK_DATABASE['customers'])
        }
    elif 'usa' in query_lower or ('customer' in query_lower and 'america' in query_lower):
        usa_customers = [c for c in MOCK_DATABASE['customers'] if c['country'] == 'USA']
        return {
            'sql': 'SELECT * FROM customers WHERE country = "USA";',
            'results': usa_customers,
            'row_count': len(usa_customers)
        }
    elif 'order' in query_lower and ('all' in query_lower or 'list' in query_lower):
        return {
            'sql': 'SELECT * FROM orders;',
            'results': MOCK_DATABASE['orders'],
            'row_count': len(MOCK_DATABASE['orders'])
        }
    elif 'high' in query_lower and 'order' in query_lower:
        high_orders = [o for o in MOCK_DATABASE['orders'] if o['amount'] > 100]
        return {
            'sql': 'SELECT * FROM orders WHERE amount > 100;',
            'results': high_orders,
            'row_count': len(high_orders)
        }
    elif 'total' in query_lower and ('order' in query_lower or 'count' in query_lower):
        return {
            'sql': 'SELECT COUNT(*) as total_orders FROM orders;',
            'results': [{'total_orders': len(MOCK_DATABASE['orders'])}],
            'row_count': 1
        }
    elif 'alice' in query_lower or 'customer' in query_lower and 'detail' in query_lower:
        alice = [c for c in MOCK_DATABASE['customers'] if c['name'].lower() == 'alice johnson']
        alice_orders = [o for o in MOCK_DATABASE['orders'] if o['customer_id'] == 1]
        return {
            'sql': 'SELECT c.*, o.* FROM customers c JOIN orders o ON c.id = o.customer_id WHERE c.name = "Alice Johnson";',
            'results': {'customer': alice, 'orders': alice_orders},
            'row_count': len(alice_orders)
        }
    else:
        return {
            'sql': 'SELECT * FROM customers LIMIT 5;',
            'results': MOCK_DATABASE['customers'][:5],
            'row_count': 5,
            'note': 'Query interpretation: Showing sample customers'
        }

@app.route('/api/query', methods=['POST'])
def query_database():
    """Natural language query to database"""
    try:
        data = request.json
        nl_query = data.get('query', '')
        
        if not nl_query:
            return jsonify({"error": "No query provided"}), 400
        
        result = process_natural_language_query(nl_query)
        
        return jsonify({
            "status": "success",
            "query": nl_query,
            "sql_generated": result['sql'],
            "results": result['results'],
            "row_count": result['row_count'],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/samples', methods=['GET'])
def get_sample_queries():
    """Get sample queries for users to try"""
    return jsonify({
        "samples": [
            {"prompt": "Show me all customers", "description": "Retrieve all customer records"},
            {"prompt": "List customers from USA", "description": "Filter customers by country"},
            {"prompt": "Show all orders", "description": "Retrieve all orders"},
            {"prompt": "High value orders", "description": "Orders over $100"},
            {"prompt": "Total number of orders", "description": "Count all orders"},
            {"prompt": "Alice's orders", "description": "Orders by specific customer"},
        ]
    })

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get database schema"""
    return jsonify({
        "tables": {
            "customers": ["id", "name", "email", "country", "signup_date"],
            "orders": ["id", "customer_id", "product", "amount", "date", "status"]
        }
    })

if __name__ == '__main__':
    app.run(debug=False, port=5007, use_reloader=False)
