from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    #expense_date : date
    amount : float
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date: date


app = FastAPI()

@app.get("/expenses/{expense_date}", response_model= List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}

@app.post("/analytics/")
def get_analytics(date_range : DateRange):
    data = db_helper.fetch_expenses_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code = 500, detail = "Failed to retreive expense summary from the datebase")

    total = sum([row['total'] for row in data])

    breakdown_category = {}
    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown_category[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown_category

@app.post("/analytics_months/")
def get_analytics_months(date_range : DateRange):
    data = db_helper.fetch_monthly_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code = 500, detail = "Failed to retreive expense month_summary from the datebase")

    #Total = sum([row['Total'] for row in data])

    breakdown_months = {}
    for row in data:

        breakdown_months[row['Month']] = {
            "Month Name": row['Month Name'],
            "Total": row['Total']

        }

    return breakdown_months

