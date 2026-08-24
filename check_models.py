import google.generativeai as genai

genai.configure(api_key="AIzaSyCklg97UcmE-oBfEoIta2AxcdNzQlPhqX4")

print("Available Models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
