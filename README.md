# ResumeTailor 🤖📄
ResumeTailor is an intelligent, multi-agent chatbot designed to help users automatically tailor their resumes for specific job descriptions. Leveraging a sophisticated multi-agent architecture built with Google's ADK (Agent Development Kit), this application analyzes, refines, and reviews a user's resume to maximize its alignment with a target role, providing actionable feedback and a tailored document ready for submission.

## ✨ Features

- **Interactive Chat Interface**: A clean and user-friendly web interface built with Streamlit for seamless user interaction.
- **Flexible Document Handling**: Accepts resumes and job descriptions as PDF, DOCX, or TXT files, or as directly pasted text.
- **Multi-Agent Architecture**: Utilizes a team of specialized AI agents to handle distinct parts of the resume tailoring process, ensuring high-quality results.
- **Iterative Refinement**: The system automatically iterates on the resume, using feedback from a Reviewer agent to improve the document until it meets a high standard (a score of 90/100) or reaches a set attempt limit.
- **Stateful Sessions**: Manages user sessions and state, allowing for a coherent, multi-turn conversation.


## 🏛️ System Architecture
ResumeTailor employs a hierarchical multi-agent system where a central Manager agent orchestrates a team of specialized sub-agents. This separation of concerns allows each agent to be an expert at its specific task.

1. **Manager Agent** `(manager/agent.py)`: The "brain" of the operation. It receives the user's initial request and delegates tasks to the appropriate sub-agents in a logical sequence. It manages the iterative loop of tailoring and reviewing.
2. **Analysis Agent** `(sub_agents/analysis_agent/)`: The "researcher." This agent's sole responsibility is to parse the user's resume and the job description. It extracts key skills, relevant experiences, and important keywords that are crucial for alignment.
3. **Tailoring Agent** `(sub_agents/tailoring_agent/)`: The "writer." This agent takes the original resume and the insights from the Analysis Agent to rewrite and rephrase sections of the resume, ensuring it speaks directly to the requirements of the job description.
4. **Review Agent** `(sub_agents/review_agent/)`: The "critic." After the Tailoring Agent produces a new version of the resume, this agent evaluates it, providing a quantitative score (out of 100) and qualitative feedback for improvement.

This entire workflow is managed within the ADK's `Runner`, which handles the session state and the flow of information between agents.

## 🚀 Getting Started
Follow these instructions to set up and run the ResumeTailor application on your local machine.

#### Prerequisites
- Python 3.9 or higher
- A Google AI API Key with the Gemini models enabled

#### Steps
1. **Clone the Repository**
    ```
    git clone [https://github.com/THEAKS1/ResumeTailor.git](https://github.com/THEAKS1/ResumeTailor.git)
    cd ResumeTailor
    ```
2. **Set Up a Virtual Environment**\
It is highly recommended to use a virtual environment to manage dependencies.
    ```
    # For Windows
    python -m venv .venv
    .\.venv\Scriptsctivate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. **Install Dependencies**\
Install all the required Python packages using the requirements.txt file.
    ```
    pip install -r requirements.txt
    ```
4. **Configure Environment Variables**\
Create a .env file in the root directory of the project by copying the example file.
    ```
    cp .env.example .env
    ```
    Now, open the .env file and add your Google AI API Key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
5. **Run the Application**\
Launch the Streamlit web server with the following command:
    ```
    streamlit run app.py
    ```
Your web browser should automatically open to the application's login screen. You can now start interacting with the ResumeTailor chatbot!

## 🛠️ Code Structure
Here is an overview of the key files and directories in the project:
```
ResumeTailor/
│
├── 📂 ResumeTailor/             # Main Python package for the agent logic
│   ├── 📂 manager/               # Contains the orchestrating Manager Agent
│   └── 📂 sub_agents/            # Contains the specialized sub-agents
│       ├── 📂 analysis_agent/
│       ├── 📂 review_agent/
│       └── 📂 tailoring_agent/
│
├── 📜 app.py                    # The main Streamlit front-end application
├── 📜 main_run_file.py          # Backend logic to run the ADK session and agent
├── 📜 config.py                 # Configuration settings (e.g., model names)
├── 📜 requirements.txt          # Project dependencies
├── 📜 .env                      # Environment variables (API Key)
└── 📜 README.md                 # This file
```

## 💡 Future Improvements
- **Enhanced Frontend**: Add features like a side-by-side resume comparison view.
- **Support for More File Types**: Include support for .rtf and other document formats.
- **Fine-Tuning**: Fine-tune the underlying LLMs on a dataset of successful resumes for even better performance.
- **Database Integration**: Store user session data in a persistent database instead of in-memory.

## 📷 Sample ScreenShots
1. **Login Screeen**
![alt text](<Login Screen.png>)

2. **Chat Screen**
![alt text](<Chat Screen.png>)