import os
from io import BytesIO

import google.generativeai as genai
import pandas as pd
import psycopg2
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer
from semantic_router.route import Route

# Load environment variables from .env file
load_dotenv()

# Load environment variables
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
GEMINI_AI_KEY = os.getenv("GEMINI_AI_KEY")


# Initialise Gemini AI model
def initialise_gemini_ai(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    return model


# Connect to PostgreSQL
def connect_to_db(dbname, user, password, host):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


# Get schema details from the database
def get_schema_details(connection, schema="public"):
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = %s;
            """,
            (schema,),
        )
        schema_details = cursor.fetchall()
        cursor.close()
        return schema_details
    except Exception as e:
        st.error(f"Error fetching schema details: {e}")
        return []


# Format schema details for display
def format_schema(schema_details):
    return ", ".join(
        [
            f"{table} has {column} of type {dtype}"
            for table, column, dtype in schema_details
        ]
    )


# Define routes for semantic routing
sql_query_route = Route(
    name="sql_query",
    utterances=[
        "show me all the watches from Rolex",
        "list the price history of Omega Seamaster",
        "find the latest news about Breitling",
        "retrieve the details of the Tag Heuer Carrera",
        "fetch the information about the most expensive watch",
        "can you show me the top 10 best-selling watches",
        "what are the latest trends in watch prices",
        "give me the summary of the latest watch releases",
        "display the details of vintage Patek Philippe watches",
        "how have the prices of Audemars Piguet watches changed over the years",
        "show the reviews of the latest watch models",
        "list the watches released in 2023",
        "find the total number of watches available from Seiko",
        "retrieve the list of watches with the highest ratings",
        "fetch the recent news about watch industry trends",
    ],
)


general_query_route = Route(
    name="general_query",
    utterances=[
        "*",  # This matches any input
    ],
)

chitchat = Route(
    name="chitchat",
    utterances=[
        "how's the weather today?",
        "how are things going?",
        "lovely weather today",
        "the weather is horrendous",
        "let's go to the chippy",
    ],
)

# Initialise the encoder and RouteLayer
encoder = HuggingFaceEncoder()
routes = [
    sql_query_route,
    general_query_route,
    chitchat,
]
rl = RouteLayer(encoder=encoder, routes=routes)


# Main function to orchestrate the application
def main():
    conn = connect_to_db(dbname, user, password, host)
    if not conn:
        return

    model = initialise_gemini_ai(GEMINI_AI_KEY)
    schema_details = get_schema_details(conn)
    formatted_schema = format_schema(schema_details)

    st.title("Chrono Watch Prediction and Chatbot")

    query_params = st.query_params
    page = query_params.get("page", ["upload"])[0]

    if page == "upload":
        handle_upload_page(conn, model, formatted_schema)
    else:
        handle_chatbot_page(conn, model, formatted_schema)

    conn.close()


# Handle the upload page functionality
def handle_upload_page(conn, model, formatted_schema):
    st.header("Upload an image of a watch")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(
                uploaded_file, caption="Uploaded Watch Image", use_column_width=True
            )
        with col2:
            st.write("## Prediction Result")
            files = {"image": uploaded_file.getvalue()}
            try:
                response = requests.post("http://localhost:5001/predict", files=files)
                if response.status_code == 200:
                    prediction = response.json()
                    st.session_state.predicted_class = prediction["predicted_class"]
                    st.session_state.predicted_price = prediction["price"]
                    st.session_state.image = uploaded_file.getvalue()

                    st.write(f"Predicted Brand: {st.session_state.predicted_class}")
                    st.write(f"Price: {st.session_state.predicted_price}")

                    if st.button(
                        "Do you want to use our chatbot to ask a few questions about this watch?"
                    ):
                        st.query_params = {"page": "chatbot"}
                else:
                    st.error("Prediction request failed.")
            except Exception as e:
                st.error(f"Error making prediction request: {e}")


# Handle the chatbot page functionality
def handle_chatbot_page(conn, model, formatted_schema):
    if (
        "predicted_class" in st.session_state
        and "predicted_price" in st.session_state
        and "image" in st.session_state
    ):
        predicted_class = st.session_state.predicted_class
        predicted_price = st.session_state.predicted_price
        image_data = st.session_state.image

        st.header("Watch Details")
        col1, col2 = st.columns([1, 2])
        with col1:
            image = Image.open(BytesIO(image_data))
            st.image(image, caption="Uploaded Watch Image", use_column_width=True)
        with col2:
            st.write(f"Predicted Brand:  {predicted_class}")
            st.write(f"Price:  {predicted_price}")

        if "conversation" not in st.session_state:
            st.session_state.conversation = []

        st.header("Chat with our AI about this Watch")
        user_question = st.text_input("Enter your question about the watch")

        if st.button("Ask"):
            route = rl(user_question)
            if route.name == "sql_query":
                handle_sql_query(
                    user_question,
                    predicted_class,
                    predicted_price,
                    formatted_schema,
                    conn,
                    model,
                )
            else:
                handle_direct_ai_response(
                    user_question,
                    predicted_class,
                    predicted_price,
                    formatted_schema,
                    model,
                )

        display_conversation_history()
    else:
        st.error("No watch data found. Please go back and upload an image.")


# Handle user question with SQL query generation
def handle_sql_query(
    user_question, predicted_class, predicted_price, formatted_schema, conn, model
):
    conversation_history = "\n".join(
        [
            f"User: {chat['question']}\nAI: {chat['response']}"
            for chat in st.session_state.conversation
        ]
    )

    prompt = f"""
    Generate an SQL query for the following question:
    '{user_question}'

    The target database has the following schema: {formatted_schema}.

    If question specifies the {predicted_class} then feel free to use this information, if needed: 
    Watch Details: Brand - {predicted_class}, Price - {predicted_price}
    """
    try:
        response = model.generate_content(prompt)
        generated_sql = (
            response.text.strip().replace("```sql", "").replace("```", "").strip()
        )

        result_df = pd.read_sql(generated_sql, conn)
        if result_df.empty:
            raise ValueError("No data returned from the database")

        query_result = result_df.to_json(orient="records")

        summary_prompt = f"""
        Based on the SQL query:
        '{generated_sql}'
        that was generated to answer the question:
        '{user_question}'
        and produced the result:
        {query_result}
        please summarise the findings in a comprehensive and contextual manner.
        Watch Details: Brand - {predicted_class}, Price - {predicted_price}
        Simply provide a brief and concise answer, without unnecessary details.
        """
        summary_response = model.generate_content(summary_prompt)
        ai_response = summary_response.text.strip()

        st.session_state.conversation.append(
            {
                "question": user_question,
                "sql_query": generated_sql,
                "query_result": query_result,
                "response": ai_response,
            }
        )

    except Exception:
        no_data_response = """
        No data was found in our database for your query. Let me find the information for you.
        """
        ai_direct_prompt = f"""
        '{user_question}'
        Here is the previous conversation context:
        {conversation_history}
        Watch Details: Brand - {predicted_class}, Price - {predicted_price}
        Please provide a comprehensive answer.
        Just answer the question in a short manner, no need to talk too much.
        Be helpful don't give answers that do help the user like "do research", "I don't know" and so on.
        """
        ai_direct_response = model.generate_content(ai_direct_prompt).text.strip()

        st.session_state.conversation.append(
            {
                "question": user_question,
                "sql_query": None,
                "query_result": no_data_response,
                "response": ai_direct_response,
            }
        )


# Handle direct AI response
def handle_direct_ai_response(
    user_question, predicted_class, predicted_price, formatted_schema, model
):
    conversation_history = "\n".join(
        [
            f"User: {chat['question']}\nAI: {chat['response']}"
            for chat in st.session_state.conversation
        ]
    )

    ai_direct_prompt = f"""
    '{user_question}'
    Here is the previous conversation context:
    {conversation_history}
    Watch Details: Brand - {predicted_class}, Price - {predicted_price}
    Please provide a comprehensive answer.
    Just answer the question in a short manner, no need to talk too much.
    Be helpful, don't give answers that do not help the user like "do research", "I don't know" and so on.
    """
    ai_direct_response = model.generate_content(ai_direct_prompt).text.strip()

    st.session_state.conversation.append(
        {
            "question": user_question,
            "sql_query": None,
            "query_result": None,
            "response": ai_direct_response,
        }
    )


# Display conversation history
def display_conversation_history():
    for chat in st.session_state.conversation:
        st.write(f"User: {chat['question']}")
        if chat["sql_query"]:
            st.write(f"Generated SQL Query: `{chat['sql_query']}`")
        if chat["query_result"]:
            st.write(f"Query Result: {chat['query_result']}")
        st.write(f"AI: {chat['response']}")
        st.write("---")


if __name__ == "__main__":
    main()
