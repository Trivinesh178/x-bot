import httpx

API_URL = "https://api.x.ai/v1/chat/completions"


class GrokError(Exception):
    pass


class GrokClient:
    def __init__(self, api_key, model, system_prompt, max_tokens=1024, transport=None):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.http = httpx.AsyncClient(timeout=60, transport=transport)

    async def ask(self, history):
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "system", "content": self.system_prompt}] + history,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            resp = await self.http.post(API_URL, json=payload, headers=headers)
        except httpx.HTTPError:
            raise GrokError("Couldn't reach the Grok API, try again in a bit.")

        if resp.status_code == 401:
            raise GrokError("The xAI API key was rejected. Check XAI_API_KEY.")
        if resp.status_code == 429:
            raise GrokError("Rate limit or credits problem on the xAI account.")
        if resp.status_code >= 400:
            raise GrokError(f"Grok API error ({resp.status_code}).")

        try:
            text = resp.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, ValueError):
            raise GrokError("Got an unexpected reply from the Grok API.")
        return (text or "").strip() or "(empty reply)"

    async def close(self):
        await self.http.aclose()
