### Introduction: 
- Deployment Link: https://speedgpt-gen-ai-cerebras-jd.vercel.app/
- Video Link: https://drive.google.com/file/d/1mcUH2Q4lshIFwD9rYP17JofO7T10GcMB/view?usp=drivesdk

A small web app that:
- Sends the same prompt to Cerebras and to a baseline LLM (e.g., a Hugging Face endpoint running Llama)
- Measures and displays latency and response (optionally streaming tokens) side-by-side
- Produces a simple CSV/JSON results file you can show in the demo
- Tech stack used: Python, React+vite, Cerebras Api, Hugging face Api 

### Run Locally: 
```
git clone https://github.com/jaya6400/speedgpt-gen-ai-hackathon.git
cd speedgpt-gen-ai-hackathon/frontend
npm install
npm run dev

Shift to new terminal:
cd speedgpt-gen-ai-hackathon/backend 
uvicorn app:app --reload --port 8000
```

Frontend running on port: http://localhost:5173/
Backend running on port: http://127.0.0.1:8000

### Screenshot
- <Image width="1408" height="934" alt="image" src="https://github.com/user-attachments/assets/52728d4d-729c-4ea3-8d60-cdd95d0ee803" />
