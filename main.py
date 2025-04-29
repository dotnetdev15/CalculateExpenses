import pandas as pd
import matplotlib.pyplot as plt
from db_connection import get_db_connection
from reportlab.pdfgen import canvas

# Establish database connection
conn = get_db_connection()
cursor = conn.cursor()

def add_expense(category, amount, date):
    cursor.execute('''
    INSERT INTO Expenses (category, amount, date)
    VALUES(?,?,?)
    ''', (category, amount, date))
    conn.commit()
    print("Expense added successfully!")

def view_summary():
    cursor.execute('SELECT category, SUM(amount) AS total_amount FROM Expenses GROUP BY category')
    result = cursor.fetchall()

    print("\nExpenses Summary by category:")
    for row in result:
        print(f"{row[0]}: {row[1]}")

def create_bar_graph():
    query = "SELECT category, SUM(amount) AS total_amount FROM Expenses GROUP BY category"
    df = pd.read_sql_query(query, conn)

    # Check if the DataFrame is empty
    if df.empty:
        print("No data available to generate the graph.")
        return

    plt.bar(df['category'], df['total_amount'], color='skyBlue')
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_pie_chart():
    query = "SELECT category, SUM(amount) AS total_amount FROM Expenses GROUP BY category"
    df = pd.read_sql_query(query, conn)

    # Check if the DataFrame is empty
    if df.empty:
        print("No data available to generate the pie chart.")
        return

    # Generate the pie chart
    plt.pie(df['total_amount'], labels=df['category'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Expense Distribution by Category")
    plt.axis('equal')
    plt.show()

def generate_pdf():
    pdf = canvas.Canvas("expense_report.pdf")

    pdf.setFont("Helvetica-Bold",16)
    pdf.drawString(200,800, "Expense Report")

    cursor.execute("SELECT * FROM Expenses")
    result = cursor.fetchall()

    pdf.setFont("Helvetica-Bold",12)
    pdf.drawString(50,760, "Category")
    pdf.drawString(200,760, "Amount")
    pdf.drawString(350,760, "Date")

    y =740
    pdf.setFont("Helvetica",12)
    for row in result:
        pdf.drawString(50,y, str(row[1]))
        pdf.drawString(200, y, str(row[2]))
        pdf.drawString(350, y, str(row[3]))
        y -= 20

    pdf.save()
    print("PDF 'expense_report.pdf' created successfully")
def view_total_expenses_by_month():
    try:
        # SQL query to group expenses by month
        query = """
        SELECT FORMAT(date, 'yyyy-MM') AS month, SUM(amount) AS total_expenses
        FROM Expenses
        GROUP BY FORMAT(date, 'yyyy-MM')
        ORDER BY month
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Display results
        print("\nTotal Expenses by Month:")
        for row in result:
            print(f"Month: {row[0]}, Total Expenses: {row[1]}")
    except Exception as e:
        print("Error retrieving expenses by month:", e)



# def view_total_expenses_by_date(start_date,end_date):
#     query = "SELECT SUM(amount) FROM Expenses WHERE date BETWEEN ? AND ?"
#     cursor.execute(query, (start_date,end_date))
#     result = cursor.fetchone()
#     print(f"\nTotal Expenses between {start_date} and  {end_date} : {result[0] if result[0] else 0}")
def main():
    try:
        while True:
            print("\nOptions:")
            print("1: Add Expense")
            print("2: View Summary")
            print("3: Create Bar Graph")
            print("4: Create Pie Chart")
            print("5: Generate Pdf")
            print("6:View Total Expenses for specific month")
            print("7: Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                category = input("Enter category: ")
                try:
                    amount = float(input("Enter amount: "))
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
                    continue
                date = input("Enter date (YYYY-MM-DD): ")
                add_expense(category, amount, date)
            elif choice == '2':
                view_summary()
            elif choice == '3':
                create_bar_graph()
            elif choice == '4':
                create_pie_chart()
            elif choice == '5':
                generate_pdf()
            elif choice == '6':
                view_total_expenses_by_month()
            elif choice == '7':
                print("Exiting the application. Goodbye!")
                conn.close()  # Close database connection
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully.")
        conn.close()

if __name__ == "__main__":
    main()
