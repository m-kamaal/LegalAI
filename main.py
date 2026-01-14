from logger import setup_logging
from src.agents.clarifier_agent.agent_runner import run

def main():
    setup_logging()
    run()

if __name__ == "__main__":
    main()
