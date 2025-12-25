from src.agents.rag_agent import QueryRoutingAgent

def main():

    print("------ LEGALAI initiated. Ask your query ------ ")
    agent = QueryRoutingAgent()


    while True:
        try:

            user_query = input("You: ")

            response = agent.run(user_query)

            print(f"LegalAI bot:\n{response}")

        except Exception as e:
            print(e)

    
if __name__ == "__main__":
    main()
