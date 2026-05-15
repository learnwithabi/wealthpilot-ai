import sys
from supervisor.workflow import app

if __name__ == "__main__":
    print("Demo - AI Portfolio Intelligence\n")

    if len(sys.argv) > 1:
        # Passed as command-line argument: python main.py "your question"
        client_input = " ".join(sys.argv[1:])
    else:
        # Interactive prompt
        print("Enter your question (press Enter twice to submit):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        client_input = "\n".join(lines)

    if not client_input.strip():
        print("No input provided. Exiting.")
        sys.exit(1)

    print(f"\nProcessing: {client_input[:80]}{'...' if len(client_input) > 80 else ''}\n")

    try:
        result = app.invoke({
            "messages": [("user", client_input)]
        })
        print("\n" + "=" * 60)
        print("FINAL SUPERVISOR OUTPUT:")
        print("=" * 60)
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"Error during portfolio review: {e}")
        raise
