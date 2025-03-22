import requests

class OllamaClient:
    def __init__(self, host='localhost', port=11434):
        """
        Initializes the Ollama client to communicate with a locally running Ollama server.
        :param host: The hostname where Ollama is running (default: 'localhost').
        :param port: The port on which Ollama is listening (default: 11434).
        """
        self.base_url = f'http://{host}:{port}/api/generate'
    
        import requests




    def query(self, model: str, prompt: str):
        """
        Sends a request to the Ollama server and returns the response.
        :param model: The name of the model to use (e.g., 'llama2', 'mistral', etc.).
        :param prompt: The text prompt to send to the model.
        :return: The generated response from the model.
        """
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            return response.text
        except requests.exceptions.RequestException as e:
            return f'Error: {e}'



