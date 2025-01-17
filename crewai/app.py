from fastapi import FastAPI, HTTPException
from datetime import datetime
from my_crew import NewsSummaryCrew

app = FastAPI()
@app.post("/api/news-summary")
async def get_news_summary(topic: str, date: str):
    
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use dd-mm-yyyy")

    inputs = {}
    inputs['topic'] = topic
    inputs['date'] = date
    
    crew = NewsSummaryCrew()
    result = crew.crew().kickoff(inputs=inputs)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)