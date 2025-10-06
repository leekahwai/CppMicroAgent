import requests

class OllamaClient:
    def __init__(self, host='localhost', port=11434, timeout=(5, 60)):
        """
        :param host: Ollama host (default 'localhost')
        :param port: Ollama HTTP port (default 11434)
        :param timeout: (connect_timeout, read_timeout) in seconds
        """
        self.base_url = f'http://{host}:{port}/api/generate'
        # Persist connections across queries for efficiency and to avoid stalls
        self.session = requests.Session()  
        # A tuple (connect_timeout, read_timeout)
        self.timeout = timeout  

    def query(self, model: str, prompt: str):
        payload = {"model": model, "prompt": prompt}
        try:
            # specifying timeout prevents the request from hanging forever
            resp = self.session.post(
                self.base_url,
                json=payload,
                timeout=self.timeout
            )
            resp.raise_for_status()
            return resp.text

        except requests.exceptions.Timeout:
            # handle connect or read timeout
            return "Error: request to Ollama server timed out"
        except requests.exceptions.RequestException as e:
            # catch other network or HTTP errors
            return f"Error: {e}"
