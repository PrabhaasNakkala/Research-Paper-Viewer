from llama_index import QuestionAnswerPrompt, GPTVectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage, PromptHelper, LLMPredictor, SimpleDirectoryReader
from langchain import OpenAI
import os

curr_dir = os.getcwd()

os.environ["OPENAI_API_KEY"] = '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'
curr = os.getcwd()

max_input = 4096
tokens = 256
chunk_size = 600
max_chunk_overlap = 20

prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name='text-davinci-003', max_tokens=tokens))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
documents = SimpleDirectoryReader(input_files=['C:\Hacking\data.txt']).load_data()
vectorIndex = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
vectorIndex.storage_context.persist(persist_dir="./storage")
response = ''


storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(service_context=service_context, storage_context=storage_context)
query_str = 'List 8 complicated and uncommon words from this pdf file. Every word MUST be over 3 letters. Separate the word and definition by a colon. End each definition with a period. Definition should be 1 sentence only. Dont list the words by number.'
QA_PROMPT_TMPL = (
    "Context Below.\n"
    "{context_str}"
    "\n"
    "Answer this qustion: {query_str}\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
query_engine = index.as_query_engine(
    text_qa_template=QA_PROMPT
)
response = query_engine.query(query_str)
print(f'Response: {response} \n')

