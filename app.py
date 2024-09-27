# app.py

from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)  # Create a Flask application instance

# Mock function to simulate fair value calculation
def calculate_fair_value(data):
    years = int(data['exit_years'])
    cagr = float(data['revenue_cagr'])
    npm = float(data['net_profit_margin'])
    pe = float(data['exit_pe'])
    so = float(data['shares_outstanding'])
    revenues = float(data['revenue'])
    discount_rate = float(data['discount_rate'])

    revenue_list = []
    profit_list = []
    for i in range(years+1):
        revenue_list.append(0)
        profit_list.append(0)
    
    for i in range(years+1):
        if i == 0:
            revenue_list[i] = revenues
        else:
            revenue_list[i] = revenues*(1+cagr)
            revenues = revenue_list[i]
        profit_list[i] = revenues*npm
    
    print(revenue_list)
    print(profit_list)
    exit_mc = profit_list[-1]*pe
    exit_price_est = exit_mc/so
    pt = exit_price_est / ((1+discount_rate) ** years)

    analysis = {'Exit Market Cap': '%0.2f' % (exit_mc), 'Exit Price Estimate': '%0.2f' % (exit_price_est), 
    'Fair value': '%0.2f' % (pt), 'Exit year profit': '%0.2f' % (profit_list[-1])}

    return analysis # Simplified calculation for demonstration

# Route for stock analysis and fair value calculation
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()['formData']  # Get JSON data from the request
    print(data)
    ticker = data['ticker']
    
    # Calculate fair value
    fair_value = calculate_fair_value(data)
    
    print(fair_value)
    # Return the results as JSON
    return jsonify(fair_value)

# Route for generating and downloading PDF
@app.route('/api/pdf/<ticker>')
def generate_pdf(ticker):
    # In a real application, you would generate a PDF here
    # For now, we'll just return a text file
    content = f"Analysis for {ticker}\n\nThis is a placeholder for the PDF content."
    
    # Write content to a temporary file
    with open("temp.txt", "w") as f:
        f.write(content)
    
    # Send the file to the client
    return send_file("temp.txt", as_attachment=True, download_name=f"{ticker}_analysis.txt")

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode