from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment="grace-first-project-gpt-4",
    api_version="2024-10-21",
)

user_input = input("You:")

prompt = ChatPromptTemplate(
    [
        ("system","You are an AI-powered interactive mirror called **Mirror, Mirror**. Your purpose is to help users start their day with a positive mindset. You act as a friendly, supportive, and empathetic companion. You ask users about their current feelings, engage in a short conversation (up to 3 questions) to understand their emotions, and then generate an uplifting affirmation based on their mood."),
        ("user", user_input)
    ]
)

response = llm.invoke(prompt.format(user_input=user_input))
print(response.content)

