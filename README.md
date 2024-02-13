## Installation Process

```sh
pip install -r requirements.txt
```

## Running the App

After installing all requirements, add OpenAI API key to the secrets,
or input it in the sidebar every time this page is visited.


Add secrets to `.streamlit/secrets.toml` in the following format:

```toml
OPENAI_API_KEY = "sk-..."
```

Run application using the following command:

```sh
streamlit run app.py
```
