# AI-Agent_Trip_Chatbot

# ✈️ TravelAI — AI Travel Planning Agent

TravelAI is an **AI-powered travel planning application** built with Python, FastAPI, LangGraph, LangChain, Groq, Tavily, and a flight search API.

The application accepts a natural-language travel request such as:

> "Plan a 7 days Japan trip from Bangladesh"

The AI agent then searches for flight information, finds hotel suggestions, creates a day-by-day itinerary, estimates the travel plan, and generates a final travel recommendation.

---

## 🚀 Features

* ✈️ Flight search using a flight API
* 🏨 Hotel search using Tavily
* 🤖 AI-powered travel planning with Groq
* 🧠 LangGraph multi-agent workflow
* 🗓️ Automatic day-by-day itinerary
* 💰 Budget-aware recommendations
* 💾 SQLite checkpointing
* 🧵 Conversation/thread management
* 🌐 FastAPI backend
* 🎨 HTML + CSS frontend
* ⚡ JavaScript API integration
* 📱 Responsive UI
* 🔄 Loading/progress interface

---

# 🏗️ Project Architecture

```text
User
 │
 ▼
┌──────────────────────────────┐
│       HTML / CSS UI          │
│       TravelAI Frontend      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        JavaScript            │
│       POST /plan             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│          app.py              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        LangGraph             │
│      Travel AI Agent         │
└──────────────┬───────────────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   ✈️ Flight  🏨 Hotel  🗓️ Itinerary
     Agent     Agent       Agent
       │        │            │
       ▼        ▼            ▼
 Flight API  Tavily       Groq LLM
       │        │            │
       └────────┼────────────┘
                ▼
        🤖 Final Agent
                │
                ▼
          JSON Response
                │
                ▼
        TravelAI Frontend
```

---

# 📁 Folder Structure

```text
travel-ai-agent/
│
├── app.py
├── travel_agent.py
├── travel.db
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── tools/
│   ├── __init__.py
│   ├── flight_tool.py
│   └── tavily_tool.py
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

---

# 📌 File Description

## `travel_agent.py`

This is the main AI backend.

It contains:

* Groq LLM
* LangGraph state
* Flight Agent
* Hotel Agent
* Itinerary Agent
* Final Response Agent
* SQLite checkpointing
* LangGraph workflow
* `run_travel_agent()` function

The main workflow is:

```text
START
  ↓
Flight Agent
  ↓
Hotel Agent
  ↓
Itinerary Agent
  ↓
Final Agent
  ↓
END
```

---

# ✈️ Flight Agent

The Flight Agent receives the user's travel request and calls the flight search tool.

```python
def flight_agent(state: TravelState):

    query = state["user_query"]

    flight_data = search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(
                content="Flight results fetched."
            )
        ],
        "llm_calls": state.get(
            "llm_calls", 0
        ) + 1
    }
```

The actual flight search logic is located in:

```text
tools/flight_tool.py
```

---

# 🏨 Hotel Agent

The Hotel Agent uses Tavily to search for hotel information.

```python
def hotel_agent(state: TravelState):

    query = f"Best hotels for {state['user_query']}"

    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(
                content="Hotel information fetched."
            )
        ],
        "llm_calls": state.get(
            "llm_calls", 0
        ) + 1
    }
```

The Tavily integration is located in:

```text
tools/tavily_tool.py
```

---

# 🗓️ Itinerary Agent

The Itinerary Agent receives:

* User request
* Flight results
* Hotel results

It then sends this information to Groq to create a practical travel itinerary.

```python
response = llm.invoke([
    SystemMessage(
        content="You are an expert travel planner."
    ),
    HumanMessage(content=prompt)
])
```

The output is stored in:

```python
state["itinerary"]
```

---

# 🤖 Final Agent

The Final Agent combines all information:

```text
User Request
     +
Flights
     +
Hotels
     +
Itinerary
     ↓
Groq
     ↓
Final Travel Recommendation
```

The final response contains:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Day-by-Day Itinerary
5. Estimated Budget
6. Final Recommendations

---

# 🧠 LangGraph State

The application uses a `TravelState` object:

```python
class TravelState(TypedDict):

    messages: Annotated[
        list[AnyMessage],
        operator.add
    ]

    user_query: str

    flight_results: str

    hotel_results: str

    itinerary: str

    llm_calls: int
```

This state is passed between the agents.

---

# 💾 SQLite Checkpoint

The project uses SQLite to store LangGraph checkpoints.

```python
conn = sqlite3.connect(
    database="travel.db",
    check_same_thread=False
)

checkpoint = SqliteSaver(conn)
```

A unique thread ID is created for each travel request:

```python
thread_id = f"user_{uuid.uuid4().hex}"
```

This allows LangGraph to maintain state for different conversations.

---

# 🌐 FastAPI Backend

The `app.py` file connects the AI backend to the frontend.

It provides two main routes.

## Home Page

```text
GET /
```

This loads:

```text
templates/index.html
```

---

## Travel Planning API

```text
POST /plan
```

Example request:

```json
{
    "user_input": "Plan a 7 days Japan trip from Bangladesh"
}
```

The backend calls:

```python
run_travel_agent(
    request.user_input
)
```

and returns JSON.

Example response:

```json
{
    "thread_id": "user_123456",
    "answer": "Here is your Japan travel plan...",
    "flight_results": "...",
    "hotel_results": "...",
    "itinerary": "...",
    "llm_calls": 4
}
```

---

# 🎨 Frontend

The frontend contains three main files:

```text
templates/
└── index.html

static/
├── css/
│   └── style.css
│
└── js/
    └── app.js
```

---

# 🖥️ HTML

The main UI is located at:

```text
templates/index.html
```

The page contains:

### Navigation

```text
TravelAI
Home
My Trips
About
```

### Hero Section

The user can enter a travel request.

Example:

```text
Plan a 7 days Japan trip from Bangladesh
```

### Quick Search

Users can quickly select:

```text
🇯🇵 Japan
🇦🇪 Dubai
🇮🇹 Italy
```

### Loading Section

The interface displays:

```text
✈️ Flight Agent
🏨 Hotel Agent
🗓️ Itinerary Agent
🤖 AI Assistant
```

### Results Section

The UI displays:

```text
Trip Summary
Flight Information
Hotel Suggestions
Day-by-Day Itinerary
AI Recommendations
```

---

# 🎨 CSS

The stylesheet is:

```text
static/css/style.css
```

It controls:

* Layout
* Colors
* Cards
* Buttons
* Navigation
* Hero section
* Loading animation
* Result cards
* Responsive design
* Mobile layout

The application uses a modern dashboard-style travel design.

---

# ⚡ JavaScript

The JavaScript file is:

```text
static/js/app.js
```

JavaScript sends the user's request to FastAPI.

```javascript
const response = await fetch("/plan", {

    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({
        user_input: query
    })

});
```

After receiving the response, JavaScript updates:

```text
AI Answer
Flight Results
Hotel Results
Itinerary
LLM Calls
```

without refreshing the page.

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

Do not commit `.env` to GitHub.

---

# 📦 Installation

## 1. Clone the project

```bash
git clone https://github.com/yourusername/travel-ai-agent.git
```

Move into the project:

```bash
cd travel-ai-agent
```

---

# 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📋 Requirements

Example `requirements.txt`:

```text
fastapi
uvicorn
python-dotenv
certifi
langgraph
langchain
langchain-core
langchain-groq
langgraph-checkpoint-sqlite
tavily-python
requests
```

Add any additional packages required by your `flight_tool.py`.

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open your browser:

```text
http://127.0.0.1:8000
```

---

# 🧪 Example Queries

You can test the application with:

```text
Plan a 7 days Japan trip from Bangladesh
```

```text
Plan a 5 days Dubai trip from Bangladesh
```

```text
Plan a 10 days Italy trip from USA
```

```text
Plan a budget trip to Thailand for 7 days
```

```text
Plan a honeymoon trip to Bali for 6 days
```

---

# 🔄 Application Workflow

When the user submits:

```text
Plan a 7 days Japan trip from Bangladesh
```

the request follows this process:

### Step 1 — Frontend

JavaScript sends:

```text
POST /plan
```

to FastAPI.

### Step 2 — FastAPI

FastAPI receives:

```python
user_input
```

and calls:

```python
run_travel_agent(user_input)
```

### Step 3 — Flight Agent

The Flight Agent searches for available flight information.

### Step 4 — Hotel Agent

The Hotel Agent searches for suitable hotels.

### Step 5 — Itinerary Agent

Groq creates a day-by-day itinerary.

### Step 6 — Final Agent

Groq combines everything into a final travel response.

### Step 7 — FastAPI

FastAPI returns JSON.

### Step 8 — JavaScript

JavaScript displays the results inside the UI.

---

# 🔐 Security

Never expose API keys inside:

```text
HTML
CSS
JavaScript
GitHub
```

Use environment variables:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

Add `.env` to `.gitignore`.

Example:

```gitignore
.env
venv/
__pycache__/
*.pyc
travel.db
```

---

# 🧩 Technologies Used

| Technology | Purpose                    |
| ---------- | -------------------------- |
| Python     | Backend                    |
| FastAPI    | API server                 |
| LangGraph  | Multi-agent workflow       |
| LangChain  | LLM framework              |
| Groq       | AI/LLM                     |
| Tavily     | Web/hotel search           |
| Flight API | Flight information         |
| SQLite     | Checkpoint storage         |
| HTML       | Frontend structure         |
| CSS        | UI styling                 |
| JavaScript | Frontend/API communication |

---

# 🚀 Future Improvements

Possible upgrades include:

* 🗺️ Interactive travel maps
* 🌦️ Weather information
* 💱 Currency conversion
* ✈️ Better flight cards
* 🏨 Hotel cards with images
* 💰 Detailed budget calculator
* 📍 Google Maps integration
* 🔐 User authentication
* 💾 Save favorite trips
* 📄 Export itinerary as PDF
* 📧 Email itinerary
* 💬 Chat-based travel assistant
* 🔄 Real-time LangGraph agent progress
* 🌐 Multi-language support
* 📱 Progressive Web App
* 🎫 Flight price alerts

---

# 🤝 Contributing

Contributions are welcome.

Fork the repository, create a new branch, make your changes, and submit a pull request.

```bash
git checkout -b feature/new-feature

git add .

git commit -m "Add new travel feature"

git push origin feature/new-feature
```

---

# ⚠️ Disclaimer

Flight availability, schedules, and pricing can change.

The application should be treated as a **travel planning assistant**, not a guaranteed booking or pricing system.

Always verify flight schedules, hotel availability, visa requirements, and final prices with the relevant provider before booking.

---

# 👨‍💻 Author

**Jubayer Hussain**

Built with Python, AI Agents, LangGraph, FastAPI, and modern web technologies.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

```text
TravelAI
AI-powered travel planning with multi-agent workflows.
```
