import json
import re
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import PromptTemplate, Settings
from llama_index.core.embeddings import resolve_embed_model
import os

from config.constants import ASPNETMVC_APP_PATH, GROQ_API_KEY, GROQ_LARGE_LANGUAGE_MODEL, ROOT_PATH, SAMPLE_METADATA_PATH

load_dotenv()
api_key = GROQ_API_KEY 


def get_sample_metadata() -> str:
    wmetadata_structure = ''
        # read json as string config/metadata_sample.json
    with open(SAMPLE_METADATA_PATH, 'r') as file:
        # read json as string config/metadata_sample
        metadata_structure = file.read()
    return metadata_structure

def groq_ingest_load(country_code, payment_method):
    query = "Generate JSON metadata based on {} and {}".format(country_code,payment_method)
    
    query = "{} and the sample json is {} and you may need to consider additional UI parameters that are not explicitly mentioned and provide attributes only when it is necessary".format(query, get_sample_metadata())
    # only load PDFs files
    required_exts = [".cs"]

    # load documents 
    loader = SimpleDirectoryReader(ASPNETMVC_APP_PATH, 
                            required_exts= required_exts,
                            recursive=True)

    documents = loader.load_data()

    # create embeddings using HuggingFace model
    embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

    # prompt template
    template =  (
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, please answer the question: {query_str}\n"
        "If you don't know the answer, please do mention : I don't know !"
    )

    prompt = PromptTemplate(template = template)

    # define llms
    llm = Groq(model=GROQ_LARGE_LANGUAGE_MODEL, api_key= api_key)

    # setting up llm and output tokens
    Settings.llm = llm
    Settings.num_output = 250
    Settings.embed_model = embed_model

    # define index
    index = VectorStoreIndex.from_documents(documents)

    # define query engine 
    query_engine = index.as_query_engine()

    # update our custom prompt
    query_engine.update_prompts(prompt)

    # Ask query and get response
    response = query_engine.query(query).response
    print("response", response)
    json_part = re.search(r'```json\n(.*?)```', response, re.DOTALL)
    print("json_part",json_part)
    if json_part:
        json_text = json_part.group(0)
        print("json_text", json_text)
        # Remove ```json markers from the start and end
        cleaned_json = json_text.strip('```json\n').strip('```')
        try:
            return cleaned_json  # Return the cleaned JSON metadata
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
    else:
        print("No JSON found in the text.")
    return ""


