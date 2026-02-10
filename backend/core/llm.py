# # import json
# # import httpx
# # from typing import Dict, Any, List
# # from openai import OpenAI
# # from core.config import settings

# # class LLMProvider:
# #     """Abstract LLM provider supporting OpenAI, Hugging Face, and Ollama"""

# #     def __init__(self):
# #         self.provider = "ollama"

# #         if self.provider == "openai":
# #             if not settings.openai_api_key:
# #                 raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
# #             self.client = OpenAI(api_key=settings.openai_api_key)
# #             self.model = settings.openai_model

# #         elif self.provider == "hf":
# #             if not settings.huggingface_api_key:
# #                 raise ValueError("HUGGINGFACE_API_KEY is required for HF provider")
# #             self.api_key = settings.huggingface_api_key
# #             self.model = settings.huggingface_model

# #         elif self.provider == "ollama":
# #             # ✅ Updated: Validate Ollama URL and model
# #             if not settings.ollama_base_url:
# #                 raise ValueError("OLLAMA_BASE_URL is required for Ollama provider (default: http://localhost:11434)")
# #             self.base_url = settings.ollama_base_url.rstrip('/')
# #             self.model = settings.ollama_model or "llama3.2"  # Default to lightweight model
# #             self._validate_ollama_connection()  # Health check on init

# #         else:
# #             raise ValueError(f"Unknown LLM provider: {self.provider}")

# #     async def _validate_ollama_connection(self):
# #         """Test Ollama connection on startup"""
# #         try:
# #             async with httpx.AsyncClient(timeout=10.0) as client:
# #                 resp = await client.get(f"{self.base_url}/api/tags")
# #                 resp.raise_for_status()
# #                 models = resp.json().get("models", [])
# #                 model_names = [m["name"] for m in models]
# #                 if self.model not in model_names:
# #                     print(f"⚠️ Warning: Model '{self.model}' not found. Available: {model_names[:5]}...")
# #         except Exception as e:
# #             raise ValueError(f"Ollama not running at {self.base_url}? Error: {str(e)}")

# #     async def chat(self, messages: List[Dict[str, str]], temperature: float = None) -> str:
# #         """Send messages to LLM and get response"""
# #         temp = temperature if temperature is not None else settings.agent_temperature

# #         if self.provider == "openai":
# #             return await self._openai_chat(messages, temp)
# #         elif self.provider == "hf":
# #             return await self._hf_chat(messages, temp)
# #         elif self.provider == "ollama":
# #             return await self._ollama_chat(messages, temp)

# #     async def _openai_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
# #         """OpenAI Chat Completion"""
# #         try:
# #             response = self.client.chat.completions.create(
# #                 model=self.model,
# #                 messages=messages,
# #                 temperature=temperature,
# #                 max_tokens=2000
# #             )
# #             return response.choices[0].message.content
# #         except Exception as e:
# #             raise Exception(f"OpenAI API error: {str(e)}")

# #     async def _hf_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
# #         """Hugging Face Inference API"""
# #         prompt = self._messages_to_prompt(messages)

# #         url = f"https://api-inference.huggingface.co/models/{self.model}"
# #         headers = {"Authorization": f"Bearer {self.api_key}"}

# #         payload = {
# #             "inputs": prompt,
# #             "parameters": {
# #                 "temperature": temperature,
# #                 "max_new_tokens": 2000,
# #                 "return_full_text": False
# #             }
# #         }

# #         async with httpx.AsyncClient(timeout=60.0) as client:
# #             try:
# #                 response = await client.post(url, headers=headers, json=payload)
# #                 response.raise_for_status()
# #                 result = response.json()

# #                 if isinstance(result, list) and len(result) > 0:
# #                     return result[0].get("generated_text", "")
# #                 return str(result)
# #             except Exception as e:
# #                 raise Exception(f"Hugging Face API error: {str(e)}")

# #     async def _ollama_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
# #         """✅ Updated Ollama Chat - Robust handling"""
# #         url = f"{self.base_url}/api/chat"

# #         payload = {
# #             "model": self.model,
# #             "messages": messages,
# #             "stream": False,
# #             "options": {
# #                 "temperature": temperature,
# #                 "num_predict": 2000,  # Max tokens
# #                 "top_p": 0.9
# #             }
# #         }

# #         async with httpx.AsyncClient(timeout=120.0) as client:
# #             try:
# #                 response = await client.post(url, json=payload)
# #                 response.raise_for_status()
# #                 result = response.json()

# #                 # Better error handling for Ollama response
# #                 if "error" in result:
# #                     raise Exception(f"Ollama error: {result['error']}")
# #                 return result.get("message", {}).get("content", "")
# #             except httpx.TimeoutException:
# #                 raise Exception("Ollama timeout - increase resources or use lighter model")
# #             except Exception as e:
# #                 raise Exception(f"Ollama API error: {str(e)}")

# #     def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
# #         """Convert chat messages to a single prompt string for HF"""
# #         prompt_parts = []
# #         for msg in messages:
# #             role = msg["role"]
# #             content = msg["content"]
# #             if role == "system":
# #                 prompt_parts.append(f"System: {content}")
# #             elif role == "user":
# #                 prompt_parts.append(f"User: {content}")
# #             elif role == "assistant":
# #                 prompt_parts.append(f"Assistant: {content}")

# #         prompt_parts.append("Assistant:")
# #         return "\n\n".join(prompt_parts)

# # # Global LLM instance
# # llm = LLMProvider()

# import json
# import httpx
# from typing import Dict, Any, List
# from openai import OpenAI
# from core.config import settings


# class LLMProvider:
#     """Abstract LLM provider supporting OpenAI, Hugging Face, and Ollama"""

#     def __init__(self):
#         self.provider = settings.llm_provider.lower()

#         if self.provider == "openai":
#             if not settings.openai_api_key:
#                 raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
#             self.client = OpenAI(api_key=settings.openai_api_key)
#             self.model = settings.openai_model

#         elif self.provider == "hf":
#             if not settings.huggingface_api_key:
#                 raise ValueError("HUGGINGFACE_API_KEY is required for HF provider")
#             self.api_key = settings.huggingface_api_key
#             self.model = settings.huggingface_model

#         elif self.provider == "ollama":
#             # Validate Ollama configuration
#             if not settings.ollama_base_url:
#                 raise ValueError("OLLAMA_BASE_URL is required for Ollama provider")

#             # Clean up base URL
#             self.base_url = settings.ollama_base_url.rstrip('/')
#             self.model = settings.ollama_model or "llama3.2"

#             # Synchronous validation on init
#             import requests
#             try:
#                 response = requests.get(f"{self.base_url}/api/tags", timeout=10)
#                 response.raise_for_status()
#                 models_data = response.json()
#                 available_models = [m.get("name", "") for m in models_data.get("models", [])]

#                 if not available_models:
#                     print(f"⚠️  Warning: No models found in Ollama. Please run: ollama pull {self.model}")
#                 elif self.model not in available_models:
#                     print(f"⚠️  Warning: Model '{self.model}' not found. Available models: {', '.join(available_models[:5])}")
#                     print(f"    To install: ollama pull {self.model}")
#                 else:
#                     print(f"✓ Ollama connected successfully. Using model: {self.model}")

#             except requests.exceptions.RequestException as e:
#                 raise ValueError(
#                     f"Cannot connect to Ollama at {self.base_url}. "
#                     f"Please ensure Ollama is running. Error: {str(e)}\n"
#                     f"Start Ollama with: ollama serve"
#                 )
#         else:
#             raise ValueError(f"Unknown LLM provider: {self.provider}")

#     async def chat(self, messages: List[Dict[str, str]], temperature: float = None) -> str:
#         """Send messages to LLM and get response"""
#         temp = temperature if temperature is not None else settings.agent_temperature

#         if self.provider == "openai":
#             return await self._openai_chat(messages, temp)
#         elif self.provider == "hf":
#             return await self._hf_chat(messages, temp)
#         elif self.provider == "ollama":
#             return await self._ollama_chat(messages, temp)

#     async def _openai_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
#         """OpenAI Chat Completion"""
#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=temperature,
#                 max_tokens=2000
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             raise Exception(f"OpenAI API error: {str(e)}")

#     async def _hf_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
#         """Hugging Face Inference API"""
#         prompt = self._messages_to_prompt(messages)

#         url = f"https://api-inference.huggingface.co/models/{self.model}"
#         headers = {"Authorization": f"Bearer {self.api_key}"}

#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "temperature": temperature,
#                 "max_new_tokens": 2000,
#                 "return_full_text": False
#             }
#         }

#         async with httpx.AsyncClient(timeout=60.0) as client:
#             try:
#                 response = await client.post(url, headers=headers, json=payload)
#                 response.raise_for_status()
#                 result = response.json()

#                 if isinstance(result, list) and len(result) > 0:
#                     return result[0].get("generated_text", "")
#                 return str(result)
#             except Exception as e:
#                 raise Exception(f"Hugging Face API error: {str(e)}")

#     async def _ollama_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
#         """Ollama Chat API with proper error handling"""
#         url = f"{self.base_url}/api/chat"

#         payload = {
#             "model": self.model,
#             "messages": messages,
#             "stream": False,
#             "options": {
#                 "temperature": temperature,
#                 "num_predict": 2000,
#                 "top_p": 0.9
#             }
#         }

#         async with httpx.AsyncClient(timeout=180.0) as client:
#             try:
#                 response = await client.post(url, json=payload)
#                 response.raise_for_status()
#                 result = response.json()

#                 # Check for errors in response
#                 if "error" in result:
#                     raise Exception(f"Ollama error: {result['error']}")

#                 # Extract message content
#                 message_content = result.get("message", {}).get("content", "")

#                 if not message_content:
#                     raise Exception("Ollama returned empty response")

#                 return message_content

#             except httpx.TimeoutException:
#                 raise Exception(
#                     "Ollama request timed out. The model may be too large or busy. "
#                     "Try using a smaller model like 'llama3.2:1b' or increase timeout."
#                 )
#             except httpx.HTTPStatusError as e:
#                 if e.response.status_code == 404:
#                     raise Exception(
#                         f"Ollama API endpoint not found at {url}. "
#                         f"Please ensure Ollama is running with: ollama serve"
#                     )
#                 raise Exception(f"Ollama HTTP error {e.response.status_code}: {e.response.text}")
#             except Exception as e:
#                 raise Exception(f"Ollama API error: {str(e)}")

#     def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
#         """Convert chat messages to a single prompt string for HF"""
#         prompt_parts = []
#         for msg in messages:
#             role = msg["role"]
#             content = msg["content"]
#             if role == "system":
#                 prompt_parts.append(f"System: {content}")
#             elif role == "user":
#                 prompt_parts.append(f"User: {content}")
#             elif role == "assistant":
#                 prompt_parts.append(f"Assistant: {content}")

#         prompt_parts.append("Assistant:")
#         return "\n\n".join(prompt_parts)


# # Global LLM instance
# llm = LLMProvider()
import json
import httpx
from typing import Dict, Any, List
from openai import OpenAI
from core.config import settings


class LLMProvider:
    """Abstract LLM provider supporting OpenAI, Hugging Face, Ollama, and Groq"""

    def __init__(self):
        self.provider = settings.llm_provider.lower()

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model

        elif self.provider == "hf":
            if not settings.huggingface_api_key:
                raise ValueError("HUGGINGFACE_API_KEY is required for HF provider")
            self.api_key = settings.huggingface_api_key
            self.model = settings.huggingface_model

        elif self.provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("GROQ_API_KEY is required for Groq provider")
            # Groq uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1"
            )
            self.model = settings.groq_model
            print(f"✓ Groq initialized successfully. Using model: {self.model}")

        elif self.provider == "ollama":
            # Validate Ollama configuration
            if not settings.ollama_base_url:
                raise ValueError("OLLAMA_BASE_URL is required for Ollama provider")

            # Clean up base URL
            self.base_url = settings.ollama_base_url.rstrip("/")
            self.model = settings.ollama_model or "llama3.2"

            # Synchronous validation on init
            import requests

            try:
                response = requests.get(f"{self.base_url}/api/tags", timeout=10)
                response.raise_for_status()
                models_data = response.json()
                available_models = [
                    m.get("name", "") for m in models_data.get("models", [])
                ]

                if not available_models:
                    print(
                        f"⚠️  Warning: No models found in Ollama. Please run: ollama pull {self.model}"
                    )
                elif self.model not in available_models:
                    print(
                        f"⚠️  Warning: Model '{self.model}' not found. Available models: {', '.join(available_models[:5])}"
                    )
                    print(f"    To install: ollama pull {self.model}")
                else:
                    print(f"✓ Ollama connected successfully. Using model: {self.model}")

            except requests.exceptions.RequestException as e:
                raise ValueError(
                    f"Cannot connect to Ollama at {self.base_url}. "
                    f"Please ensure Ollama is running. Error: {str(e)}\n"
                    f"Start Ollama with: ollama serve"
                )
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    async def chat(
        self, messages: List[Dict[str, str]], temperature: float = None
    ) -> str:
        """Send messages to LLM and get response"""
        temp = temperature if temperature is not None else settings.agent_temperature

        if self.provider == "openai":
            return await self._openai_chat(messages, temp)
        elif self.provider == "hf":
            return await self._hf_chat(messages, temp)
        elif self.provider == "groq":
            return await self._groq_chat(messages, temp)
        elif self.provider == "ollama":
            return await self._ollama_chat(messages, temp)

    async def _openai_chat(
        self, messages: List[Dict[str, str]], temperature: float
    ) -> str:
        """OpenAI Chat Completion"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def _groq_chat(
        self, messages: List[Dict[str, str]], temperature: float
    ) -> str:
        """Groq Chat Completion (OpenAI-compatible API)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=8000,  # Groq supports higher token limits
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    async def _hf_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Hugging Face Inference API"""
        prompt = self._messages_to_prompt(messages)

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": 2000,
                "return_full_text": False,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()

                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                return str(result)
            except Exception as e:
                raise Exception(f"Hugging Face API error: {str(e)}")

    async def _ollama_chat(
        self, messages: List[Dict[str, str]], temperature: float
    ) -> str:
        """Ollama Chat API with proper error handling"""
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": 2000, "top_p": 0.9},
        }

        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()

                # Check for errors in response
                if "error" in result:
                    raise Exception(f"Ollama error: {result['error']}")

                # Extract message content
                message_content = result.get("message", {}).get("content", "")

                if not message_content:
                    raise Exception("Ollama returned empty response")

                return message_content

            except httpx.TimeoutException:
                raise Exception(
                    "Ollama request timed out. The model may be too large or busy. "
                    "Try using a smaller model like 'llama3.2:1b' or increase timeout."
                )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise Exception(
                        f"Ollama API endpoint not found at {url}. "
                        f"Please ensure Ollama is running with: ollama serve"
                    )
                raise Exception(
                    f"Ollama HTTP error {e.response.status_code}: {e.response.text}"
                )
            except Exception as e:
                raise Exception(f"Ollama API error: {str(e)}")

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert chat messages to a single prompt string for HF"""
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


# Global LLM instance
llm = LLMProvider()
