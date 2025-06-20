# pip install sentence-transformers
# uvicorn api:app --reload
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import random
import time
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
import random
import logging
logger = logging.getLogger(__name__)

api_keys = [
    os.getenv('gemini_api_key1'),
    os.getenv('gemini_api_key2'),
    os.getenv('gemini_api_key3'),
    os.getenv('gemini_api_key4'),
    os.getenv('gemini_api_key5'),
    os.getenv('gemini_api_key6')
]
# print(2)
def get_random_model():
    api_key = random.choice(api_keys)

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("models/gemini-1.5-flash")


model_emb = SentenceTransformer("nomic-ai/modernbert-embed-base")

def generate_embeddings(text):
    if isinstance(text, str):
        texts = [text]
    else:
        texts = text

    em = model_emb.encode(texts, reference_compile=False)
    
    if isinstance(text, str):
        return em[0]
    
    
logger.info("get_random_model generate_embeddings ")
pc = Pinecone(api_key="pcsk_6NTZFz_EWFY2uBqSe526iNNgyon6QTyuV2ibyZp7iiQyvg8zkDuP5SZ7pxWAiQT8xj1H49")
index_name = "quickstart"
index = pc.Index(index_name)


def semantic_search2(query, k=10):
    ans=[]
    query_e=generate_embeddings(query)
    try:
        # k=int(input("Number of top k paragraphs you want (out of 30): "))
        k=10
    except:
        print("Non valid value, k = 10 for results.")
        k=10
    # print("\n")
    print("Your chosen k is: ", k)
    results = index.query(
        vector=query_e.tolist(),
        top_k=k,
        include_metadata=True
    )
    
    for match in results.matches:
        ans.append(match["metadata"]["text"])
    ans = list(set(ans))

    return ans




logger.info("semantic search")
def genfirst(query, summ):
    prompt = f"""
You are given query. Find the most appropriate one or multiple paragraphs.
Also tell a little about each paragraph by explicitly mentioning the asked parameter in query.

Query: {query}


"""
    # print("Summarized paras: ")
    # print(summ)

    for i, para in enumerate(summ, 1):
        prompt += f"Paragraph {i}: {para}\n"
    # r=ollama(prompt)
    retries = 3 
    success = False
    
    while retries > 0 and not success:
        try:
            model = get_random_model()
            r = model.generate_content(prompt)
            success = True
            
        except Exception as e:
            retries -= 1
            if retries > 0:
                time.sleep(3)

    r=r.text
    return r



waiting_messages = [
    "Evaporating irrelevant data — condensing only what matters...",
    "Hold tight! Just ablating some knowledge from the right source.",
    "Target locked. Pulsing through dense research material...",
    "Synthesizing your solution — atom by atom.",
    "Filtering noise, amplifying the signal — your answer is forming.",
    "Gathering atoms of info… precision takes a second!",
    "Tuning parameters… the perfect reply is on its way.",
    "Just refining a few layers of thought…",
    "Your answer is almost deposited in the chamber.",
    "Reconstructing knowledge — coherence in progress.",
    "Bouncing off a few ideas… your insight is seconds away.",
    "We apologise for the delay, our bot was having a nap.",
    "Apologies for the wait! We’re just bribing the servers with coffee.",
    "Thanks for your patience!",
    "Your data is packed in a box… and the delivery guy will deliver it to you soon.",
    "Hang tight, we're getting that info for you...",
    "Just a moment — gathering the best response.",
    "Working on it… almost there!",
    "Give us a second to fetch the right answer.",
    "One sec — making sure it's accurate.",
    "Hold on… putting the pieces together.",
    "Processing your request — thanks for your patience.",
    "Looking that up… won't be long!",
    "Just checking the facts — back in a flash.",
    "Getting everything ready for you..."
]



def querygen(query):
    logger.info("genfirst querrygen")

    prompt=f"""
    You are given a query. Return only the parameters in quotes.
    Return the answer in inverted comma.
    Example: "What is temperature of X thin films over KrF laser" then return "temperature X thin films KrF laser"

    Query: {query}

    """
    retries = 3 
    success = False
    while retries > 0 and not success:
        try:
            model = get_random_model()
            r = model.generate_content(prompt)
            success = True
        except Exception as e:
            print(e)
            retries -= 1
            if retries > 0:
                time.sleep(3)

    r=r.text

    return r


def summarizer(query):
    print("You're into semantic search 🔎...")
    q=querygen(query)
    sim = semantic_search2(q)
    print("Analysing the retrieved paragraphs 🕵🏻...")
    # print("...")
    
    summ = []
    for para in sim:

        retries = 3 
        success = False

        while retries > 0 and not success:
            try:
                model = get_random_model()
                response = model.generate_content(f"""
                                                  Summarize the given text in only two lines (30 words).
                                                  Do not lose any information about parameters and materials, like temperature, wavelength, pressure, material name, substrate name, etc.
                                                  
                                                  Text:
                                                  {para}
""")
                summ.append(response.text)
                success = True
            except Exception as e:
                retries -= 1
                if retries > 0:
                    time.sleep(3)
                
    return summ

def gensecond_semantic(query):
    logger.info("gensecond semantic funciton called")
    logger.info("Thank you, We got your query✅...")
    # print("...")

    
    summ = summarizer(query)

    # print(summ)

    random_message = random.choice(waiting_messages)
    print(random_message)
    # print("...")

    r1 = genfirst(query, summ)

    # print(r1)
    print("Generating your answer✍🏻...")

    
    
    prompt = f"""
You have a query and the hint to the query about PLD (Pulsed Laser Deposition).

1. Present to me it like you didn't get any hint and you're speaking it using your data. DON'T MENTION ANYTHING ABOUT PARAGRAPHS EXPLICITLY.
2. Present every information. Dont miss anything, you have to present it in 30 to 150 words maximum, unless query asks to make it bigger.

Query: 
{query}


Hint: 
{r1}

"""

    print("--" * 60)
    retries = 3 
    success = False
    
    while retries > 0 and not success:
        try:
            model = get_random_model()
            r = model.generate_content(prompt)
            success = True
            
        except Exception as e:
            retries -= 1
            if retries > 0:
                time.sleep(3)
    
    bot_response = r.text
    # print(r.text)

    return bot_response

# print(gensecond_semantic("What is the wavelength used in MgO thin films deposition"))
def chatbot_(user_input):
    print(":hhij")
    logger.info("Begin Loading things")
    r=gensecond_semantic(user_input)
    return r
    # print("Bot said 🤖: ", r)

logger.info("summariser gensecond chatbot")