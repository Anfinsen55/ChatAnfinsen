from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

input_text= "why sky is blue"

print(genai.chat())
print("Hello World")

