import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from new import run_sqlite_query


from langchain import hub

from dotenv import load_dotenv
load_dotenv()

def lookup(nlques: str) -> str:
    llm=ChatOpenAI(temperature=0,model_name="gpt-4o")

    template="""You are an expert at converting natural language questions into SQL queries.
    Given user question {User_Question}, Convert the natural language question into a SQL query that fetches data from the cookies table. 
    You must return a **clean** SQL Query always without any extra formatting or backticks.

    The table has the following schema:
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
    When generating a SQL query, follow these rules:

    1. Always use the full expression in the `GROUP BY` clause. Do not use aliases in `GROUP BY`. For example, if you are grouping by `SUBSTR(localeCd, 0, 2)`, use `GROUP BY SUBSTR(localeCd, 0, 2)` rather than `GROUP BY country`.
    2. Always use `LIMIT` to restrict results if the query asks for top results.If not specified use 5 by default
    3. Ensure that the query selects only the relevant columns based on the user question.

    Before Returning any query, make sure you do proper formatting and only respond the query part, no extra line symbol, space or any such thing
    final alswer in the chain should be a number only not a query. if you face issue , send it to llm again an ask to provide answer in correct format which you can tell in output
    And final answer should be in form of a statement, as in asnwering user's question
     """

    prompt_template=PromptTemplate(
        template=template,
        input_variables=["User_Question"]
    )
    sql_tool = [
        Tool(
            name="Run_SQL_Query",
            func=run_sqlite_query,
            description="Runs a SQL query where user asks cookies related question",
        )
    ]
    
    react_prompt=hub.pull("hwchase17/react")
    agent=create_react_agent(llm=llm,tools=sql_tool,prompt=react_prompt)
    agent_executor= AgentExecutor(agent=agent,tools=sql_tool,verbose=True,handle_parsing_errors=True)

    result=agent_executor.invoke(
        input={"input":prompt_template.format_prompt(User_Question=nlques)},
        )
    
    nlqueryresult=result["output"]
    return nlqueryresult



if __name__ == "__main__":
    print(lookup(nlques="How many pending re runs are there in march"))