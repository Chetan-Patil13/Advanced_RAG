from backend.rag_chain import ask_rag

query = "What are the Criteria for land selection?"
response = ask_rag(query)

print("\n🔍 Response:")
print(response)
