import os
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
import pyodbc
import json
from datetime import date, datetime

# Load environment variables
load_dotenv()

print("Environment variables loaded.")


# Database connection function
def connect_to_db():
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={os.getenv("DB_SERVER")};'
        f'DATABASE={os.getenv("DB_NAME")};'
        f'UID={os.getenv("DB_USERNAME")};'
        f'PWD={os.getenv("DB_PASSWORD")}'
    )
    print(
        f"Attempting to connect to database: {os.getenv('DB_NAME')} on server: {os.getenv('DB_SERVER')}"
    )
    conn = pyodbc.connect(conn_str)
    print("Database connection successful.")
    return conn


# Function to serialize date objects
def serialize_dates(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return str(obj)


# Function to get invoices for a specific customer
def get_invoices_for_customer(customer_id):
    print(f"Fetching invoices for customer ID: {customer_id}")
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_Invoices WHERE CustomerID = ?", customer_id)
    columns = [column[0] for column in cursor.description]
    invoices = [
        dict(zip(columns, map(serialize_dates, row))) for row in cursor.fetchall()
    ]
    conn.close()
    print(f"Found {len(invoices)} invoices for customer ID: {customer_id}")
    return json.dumps(invoices)


# Function to get timesheets for a specific employee
def get_timesheets_for_employee(employee_id):
    print(f"Fetching timesheets for employee ID: {employee_id}")
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_Timesheets WHERE EmployeeID = ?", employee_id)
    columns = [column[0] for column in cursor.description]
    timesheets = [
        dict(zip(columns, map(serialize_dates, row))) for row in cursor.fetchall()
    ]
    conn.close()
    print(f"Found {len(timesheets)} timesheet entries for employee ID: {employee_id}")
    return json.dumps(timesheets)


# Define the tools for the AI agent
tools = [
    {
        "name": "get_invoices_for_customer",
        "description": "Retrieves all invoices for a specific customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The ID of the customer.",
                }
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_timesheets_for_employee",
        "description": "Retrieves all timesheets for a specific employee.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "The ID of the employee.",
                }
            },
            "required": ["employee_id"],
        },
    },
]

# Initialize ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
print("ChatOpenAI initialized.")


# Chatbot function
def chatbot(query):
    print(f"Received query: {query}")
    messages = [
        ChatMessage(
            role="system",
            content="You are a helpful assistant that can query invoice and timesheet information from test tables.",
        ),
        HumanMessage(content=query),
    ]

    print("Sending query to AI model...")
    response = llm.predict_messages(messages, functions=tools)
    print("Received response from AI model.")

    if response.additional_kwargs.get("function_call"):
        function_name = response.additional_kwargs["function_call"]["name"]
        function_args = json.loads(
            response.additional_kwargs["function_call"]["arguments"]
        )
        print(f"AI model requested function call: {function_name}")

        if function_name == "get_invoices_for_customer":
            function_response = get_invoices_for_customer(function_args["customer_id"])
        elif function_name == "get_timesheets_for_employee":
            function_response = get_timesheets_for_employee(
                function_args["employee_id"]
            )
        else:
            print(f"Error: Unknown function call - {function_name}")
            return "Error: Unknown function call."

        messages.append(AIMessage(content=response.content))
        messages.append(
            ChatMessage(
                role="function",
                content=function_response,
                additional_kwargs={"name": function_name},
            )
        )

        print("Sending function result back to AI model for final response...")
        final_response = llm.predict_messages(messages)
        print("Received final response from AI model.")
        return final_response.content
    else:
        print("AI model did not request a function call.")
        return response.content


# Gradio interface
iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
    outputs="text",
)

# Run the Gradio app
print("Starting Gradio interface...")
iface.launch(server_name="127.0.0.1", server_port=7860)
print("Gradio interface is running.")
print(
    "You can access it in your web browser at: http://127.0.0.1:7860 or http://localhost:7860"
)
