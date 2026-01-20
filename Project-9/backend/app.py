from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Mock Excel/Sheet data
SPREADSHEET_DATA = {
    'Sales': {
        'headers': ['Month', 'Product', 'Quantity', 'Revenue', 'Region'],
        'rows': [
            ['January', 'Laptop', 150, 180000, 'North'],
            ['January', 'Phone', 300, 90000, 'South'],
            ['February', 'Laptop', 180, 216000, 'North'],
            ['February', 'Phone', 250, 75000, 'South'],
            ['March', 'Laptop', 200, 240000, 'North'],
            ['March', 'Phone', 350, 105000, 'South'],
        ]
    },
    'Employees': {
        'headers': ['Name', 'Department', 'Salary', 'Hire_Date', 'Status'],
        'rows': [
            ['Alice', 'Engineering', 120000, '2022-01-15', 'Active'],
            ['Bob', 'Sales', 80000, '2023-06-20', 'Active'],
            ['Carol', 'HR', 75000, '2021-03-10', 'Active'],
            ['David', 'Engineering', 130000, '2020-09-05', 'Active'],
            ['Eve', 'Finance', 95000, '2022-11-12', 'Active'],
        ]
    }
}

def query_sheet(sheet_name, query_text):
    """Process natural language queries on spreadsheet data"""
    if sheet_name not in SPREADSHEET_DATA:
        return None
    
    sheet = SPREADSHEET_DATA[sheet_name]
    query_lower = query_text.lower()
    
    if sheet_name == 'Sales':
        if 'north' in query_lower:
            filtered = [row for row in sheet['rows'] if row[4] == 'North']
            return {'filtered_data': filtered, 'description': f'Found {len(filtered)} north region sales'}
        elif 'total revenue' in query_lower or 'sum revenue' in query_lower:
            total = sum(row[3] for row in sheet['rows'])
            return {'result': total, 'description': f'Total revenue: ${total:,}'}
        elif 'laptop' in query_lower:
            filtered = [row for row in sheet['rows'] if row[1] == 'Laptop']
            return {'filtered_data': filtered, 'description': f'Found {len(filtered)} laptop sales'}
        else:
            return {'all_data': sheet['rows'], 'description': 'Showing all sales data'}
    
    elif sheet_name == 'Employees':
        if 'engineering' in query_lower:
            filtered = [row for row in sheet['rows'] if row[1] == 'Engineering']
            return {'filtered_data': filtered, 'description': f'Found {len(filtered)} engineering employees'}
        elif 'salary' in query_lower and 'over' in query_lower:
            filtered = [row for row in sheet['rows'] if row[2] > 100000]
            return {'filtered_data': filtered, 'description': f'Employees with salary > $100k'}
        elif 'highest' in query_lower and 'salary' in query_lower:
            highest = max(sheet['rows'], key=lambda x: x[2])
            return {'result': highest, 'description': f'Highest salary: {highest[0]} - ${highest[2]:,}'}
        else:
            return {'all_data': sheet['rows'], 'description': 'Showing all employees'}
    
    return None

@app.route('/api/sheets', methods=['GET'])
def list_sheets():
    """List available spreadsheets"""
    return jsonify({
        "sheets": [
            {"name": "Sales", "description": "Monthly sales data by product and region"},
            {"name": "Employees", "description": "Employee information and salaries"}
        ]
    })

@app.route('/api/sheet/<sheet_name>', methods=['GET'])
def get_sheet(sheet_name):
    """Get sheet data"""
    if sheet_name not in SPREADSHEET_DATA:
        return jsonify({"error": "Sheet not found"}), 404
    
    sheet = SPREADSHEET_DATA[sheet_name]
    return jsonify({
        "name": sheet_name,
        "headers": sheet['headers'],
        "rows": sheet['rows'],
        "row_count": len(sheet['rows'])
    })

@app.route('/api/query-sheet', methods=['POST'])
def query():
    """Query a spreadsheet with natural language"""
    try:
        data = request.json
        sheet_name = data.get('sheet', '')
        query_text = data.get('query', '')
        
        if not sheet_name or not query_text:
            return jsonify({"error": "Missing sheet or query"}), 400
        
        result = query_sheet(sheet_name, query_text)
        
        if result is None:
            return jsonify({"error": "Sheet not found"}), 404
        
        sheet = SPREADSHEET_DATA[sheet_name]
        
        return jsonify({
            "status": "success",
            "sheet": sheet_name,
            "query": query_text,
            "headers": sheet['headers'],
            "result": result,
            "sample_queries": [
                "Show north region sales",
                "What is total revenue",
                "List laptop sales",
                "Engineering department",
                "Highest salary"
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5008, use_reloader=False)
