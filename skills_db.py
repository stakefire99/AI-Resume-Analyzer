"""
Skills Database for AI Resume Analyzer
"""

SKILLS = {
    "Programming Languages": [
        "Python", "SQL", "Java", "JavaScript", "TypeScript", "R", "C++", "C#",
        "Go", "Rust", "Scala", "MATLAB", "Kotlin", "Swift", "PHP", "Ruby", "Bash"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Feature Engineering", "Data Wrangling", "EDA",
        "Exploratory Data Analysis", "Statistical Analysis", "A/B Testing",
        "Hypothesis Testing", "Regression", "Classification", "Clustering",
        "Time Series", "Forecasting"
    ],
    "Python Libraries": [
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras",
        "OpenCV", "NLTK", "SpaCy", "Hugging Face", "Transformers",
        "Matplotlib", "Seaborn", "Plotly", "Streamlit", "Flask", "FastAPI",
        "Django", "Requests", "BeautifulSoup", "Selenium"
    ],
    "Data Visualization & BI": [
        "Power BI", "Tableau", "Looker", "Google Data Studio", "Excel",
        "Advanced Excel", "Google Sheets", "D3.js", "Bokeh", "Dash"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "BigQuery",
        "Snowflake", "DynamoDB", "Oracle", "SQLite", "Elasticsearch", "Redshift"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
        "CI/CD", "Jenkins", "GitHub Actions", "Linux", "REST API", "GraphQL"
    ],
    "Data Engineering": [
        "ETL", "Data Pipeline", "Apache Spark", "Hadoop", "Kafka",
        "Airflow", "dbt", "Data Warehouse", "Data Lake", "MLOps", "Databricks"
    ],
    "Tools": [
        "Git", "GitHub", "GitLab", "Jira", "Jupyter", "Google Colab", "VS Code"
    ],
    "AI & Generative": [
        "OpenAI API", "LangChain", "LLM", "Prompt Engineering",
        "Generative AI", "RAG", "Vector Database", "Embeddings", "Fine-tuning"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Problem Solving", "Critical Thinking",
        "Team Collaboration", "Project Management", "Agile", "Scrum"
    ]
}

ALL_SKILLS = [s for skills in SKILLS.values() for s in skills]

ALIASES = {
    "ml": "Machine Learning", "dl": "Deep Learning",
    "nlp": "Natural Language Processing", "cv": "Computer Vision",
    "sklearn": "Scikit-learn", "sk-learn": "Scikit-learn",
    "gcp": "Google Cloud", "aws": "AWS", "etl": "ETL", "eda": "EDA",
    "llm": "LLM", "genai": "Generative AI", "gen ai": "Generative AI",
    "spacy": "SpaCy", "nltk": "NLTK", "tf": "TensorFlow",
}
