from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__, static_url_path='/static', static_folder='static')

db = mysql.connector.connect(
    host = "localhost",
    user = "nishuz",
    password = "Nishchay.123",
    database = "EB_Database",
    connection_timeout=300,
    connect_timeout=30
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_by_bond.html')
def search_page():
    return render_template('search_by_bond.html')

@app.route('/search', methods=['GET'])
def search():
    bond_number = request.args.get('bond_number')
    query = "SELECT * FROM EB_Redemption_Details WHERE `Bond_Number` = %s"
    cursor.execute(query, (bond_number,))
    table1_results = cursor.fetchall()
    query = "SELECT * FROM EB_Purchase_Details WHERE `Bond_Number` = %s"
    cursor.execute(query, (bond_number,))
    table2_results = cursor.fetchall()
    search_results = {
        'table1_results': table1_results,
        'table2_results': table2_results
    }
    return render_template('search_by_bond.html', search_results=search_results)

@app.route('/filter.html')
def filter_page():
    return render_template('filter.html')

@app.route('/filter_results')
def filter_results():
    selected_table = request.args.get('table')
    selected_attribute = request.args.get('attribute')
    search_term = request.args.get('search_term')
    query = f"SELECT * FROM {selected_table} WHERE {selected_attribute} LIKE %s"
    cursor.execute(query, (f'%{search_term}%',))
    search_results = cursor.fetchall()

    html = "<table class='table'>"
    html += "<thead><tr>"
    for column in cursor.description:
        html += f"<th>{column[0]}</th>"
    html += "</tr></thead><tbody>"
    for row in search_results:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

@app.route('/bond_purchases.html')
def bond_purchases():
    return render_template('bond_purchases.html')

@app.route('/party_analysis.html')
def party_analysis():
    return render_template('party_analysis.html')

@app.route('/donation_analysis.html')
def donation_analysis():
    return render_template('donation_analysis.html')

@app.route('/get_companies')
def get_companies():
    query = "SELECT DISTINCT `Name_of_the_Purchaser` FROM `EB_Purchase_Details` ORDER BY `Name_of_the_Purchaser`"
    cursor.execute(query)
    companies = [row[0] for row in cursor.fetchall()]
    return jsonify(companies)

@app.route('/bond_purchases_data')
def bond_purchases_data():
    try:
        company = request.args.get('company')
        query = "SELECT YEAR(STR_TO_DATE(`Date_of_Purchase`, '%d/%b/%Y')) AS `Year`, COUNT(*) AS `NumberOfBonds`, SUM(CAST(REPLACE(REPLACE(REPLACE(`Denominations`, ',', ''), ' ', ''), '₹', '') AS UNSIGNED)) AS `TotalValueOfBonds` FROM `EB_Purchase_Details` WHERE `Name_of_the_Purchaser` = %s GROUP BY YEAR(STR_TO_DATE(`Date_of_Purchase`, '%d/%b/%Y'))"
        print("Bond Purchases Data Query:", query)  # Print the query to console
        cursor.execute(query, (company,))
        data = {}
        for year, numberOfBonds, totalValueOfBonds in cursor.fetchall():
            data[year] = {
                'numberOfBonds': numberOfBonds,
                'totalValueOfBonds': totalValueOfBonds
            }
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
