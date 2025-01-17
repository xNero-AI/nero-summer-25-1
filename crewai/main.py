from my_crew import NewsSummaryCrew


def main():
    input_data = {
        "topic": "política",
        "date": "01-07-2024",
    }
    
    crew = NewsSummaryCrew()
    result = crew.crew().kickoff(inputs=input_data)
    # print(result)
    
if __name__ == "__main__":
    main()