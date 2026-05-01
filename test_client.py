from services.groq_client import GroqClient

client = GroqClient()

response = client.generate_response("Explain incident management in 2 lines")

print(response)