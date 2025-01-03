import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)

    if connection.is_connected():
        print("Connection is successful")
    else:
        print("Failed to Connect")
    yield cursor
    if commit:
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM expenses "
            "WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) "
            "VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s",
                       (expense_date,))

def fetch_expenses_summary(start_date,end_date):
    logger.info(f"fetch_expenses_summary called with {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
                    '''SELECT category, Sum(amount) as total
                    FROM expenses where expense_date
                    between %s and %s
                    group by category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_expense_summary(start_date, end_date):
    logger.info(f"fetch_monthly_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
                SELECT 
                    MONTH(expense_date) AS "Month",           -- Month number as index
                    DATE_FORMAT(expense_date, '%M') AS "Month Name", -- Full month name
                    SUM(amount) AS Total                          -- Sum of amounts for the month
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s               -- Filter by date range
                GROUP BY MONTH(expense_date), DATE_FORMAT(expense_date, '%M') -- Group by month number and name
                ORDER BY MONTH(expense_date);                               -- Order by month number""",
            (start_date, end_date)
        )
        data_month = cursor.fetchall()
        return data_month

if __name__ == "__main__":
    # fetch_all_records()
    # expenses = fetch_expenses_for_date("2024-08-01")
    # print(expenses)
    #insert_expense("2024-08-25", 40, "Food", "Eat Tasty Samosa Chaat")
    #delete_expenses_for_date("2024-08-25")
    summary = fetch_monthly_expense_summary("2024-08-01","2024-09-05")
    for records in summary:
        print(records)
