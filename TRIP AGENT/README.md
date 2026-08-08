conda create -n Agents python= 3.11 -y numpy pandas scikit-learn


conda activate Agents 

pip install -r requirements.txt


Run app.py file ->to terminal: -> python app.py



langgraph-checkpoint-sqlite==3.1.0 # for sql data
langgraph==1.2.2 
langchain==1.3.2
langchain-groq==1.1.3        # LLM to use groq model
langchain-community==0.4.2  # dependece
langchain-tavily==0.2.18    # google search
python-dotenv==1.2.2        # for .env file
tavily-python==0.7.24       # dependence 
requests==2.34.2


airportsdata==20260315      # for airport data
pycountry==26.2.16
fastapi==0.136.3
uvicorn==0.48.0
jinja2==3.1.6