import sqlite3
import pandas as pd
from langchain.tools import Tool

# Correct path to your CSV file
csv_path = "/users/fnusatvik/desktop/mishwa_assignment/info.csv"

# Connect to the SQLite database (info.db)
connection = sqlite3.connect("/users/fnusatvik/desktop/mishwa_assignment/info.db")

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Create a cursor object
c = connection.cursor()

# Create the table with the correct schema
c.execute('''
CREATE TABLE IF NOT EXISTS ExecutionData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Month TEXT,
    Platform TEXT,
    TotalExecutions INTEGER,
    InvalidFailures INTEGER,
    DataIssue INTEGER,
    HeadSpin INTEGER,
    MTNIssue INTEGER,
    NRPData INTEGER,
    PendingRerun INTEGER,
    ScriptIssue INTEGER,
    SeeTest INTEGER,
    SyncIssue INTEGER,
    ThrottlingIssue INTEGER,
    Blank INTEGER
)
''')

# Load data into the table from the DataFrame
df.to_sql('info', connection, if_exists='append', index=False)

# Commit changes and close the cursor
connection.commit()

# Function to run SQLite queries
def run_sqlite_query(query):
    c = connection.cursor()
    c.execute(query)
    result = c.fetchall()
    return result

# Example usage
#query_result = run_sqlite_query("SELECT * FROM info LIMIT 5")
#print(query_result)

run_sql= Tool.from_function(
    name="run_sql_query_tool",
    description="Runs a SQlite query on executions table",
    func=run_sqlite_query
)

sql_schema="""The table has the following schema:
    Table 'info':
    The info table stores data related to execution attempts and issues across different platforms and months. Below is a breakdown of each column, its purpose, and the possible values or range for categorical variables:

    1. Month: A TEXT column indicating the month of the data record. Possible values include: 'Jan', 'Feb', 'Mar', 'Apr', 'May', etc., representing different months of the year.

    2. Platform: A TEXT column specifying the platform type where the executions took place. Possible values include:
    'Desktop': Indicates desktop platform execution.
    'MW': Likely stands for Mobile Web.
    'MVA': Possibly stands for Mobile Virtual Application.
    'FIOS': Could refer to a specific type of network or platform.
    'Spanish': Indicates a Spanish language platform or localized execution.
    
    3.Total executions: An INTEGER representing the total count of execution attempts made on the given platform during that month. (Range: varies based on the number of executions, e.g., from 0 to hundreds of thousands).

    4. Invalid Failures: An INTEGER showing the number of failed executions due to invalid reasons, like data errors or misconfigurations. (Range: typically 0 to tens of thousands).

    5.Data Issue: An INTEGER indicating the number of issues directly related to the quality or availability of data. (Range: typically 0 to thousands).

    6.HeadSpin: An INTEGER recording the number of failures or issues tied to the 'HeadSpin' tool or platform. (Range: typically 0 to a few thousand).

    7.MTN Issue: An INTEGER counting the issues categorized as 'MTN', representing specific execution problems. (Range: typically 0 to hundreds).

    8.NRP Data: An INTEGER reflecting the count of issues associated with 'NRP' data or related network issues. (Range: typically 0 to hundreds).

    9.Pending Re-run: An INTEGER that shows the number of executions pending for a re-run due to failures or incomplete processes. (Range: typically 0 to thousands).

    10.Script Issue: An INTEGER denoting problems encountered due to script errors during the execution process. (Range: typically 0 to thousands).

    11.SeeTest: An INTEGER indicating the count of issues related to the 'SeeTest' platform or testing tool. (Range: typically 0 to thousands).

    12.Sync Issue: An INTEGER representing the number of synchronization problems faced during execution. (Range: typically 0 to tens of thousands).

    13.Throttling Issue: An INTEGER recording any issues caused by throttling, which may affect performance or execution speed. (Range: typically 0 to hundreds).
     For filtering, convert the text to lowercase and then compare.
    """
