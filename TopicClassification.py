from openai import OpenAI
import os
import pickle
import requests

def interroger_llm(text):
    print(text)
    prompt = f"""Carefully analyze the following text before responding.
Then, classify it into one of these categories by giving only the category number:
1 = Genuine, non-rhetorical question seeking a real answer
2 = Statement that is clearly and entirely false, according to any specialist in the subject
3 = Statement on a topic where there is no clear or absolute truth
4 = Statement that is partially true and partially false
5 = Other (true factual statement, opinion, or neutral statement)

Text: \"{text}\" """

    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # Ou llama3-70b
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return chat_completion.choices[0].message.content.strip()

def get_reddit_post_classification(url):
    if not url.endswith('.json'):
        if url.endswith('/'):
            url += '.json'
        else:
            url += '/.json'

    headers = {'User-agent': 'Mozilla/5.0'}  # Pour éviter un blocage

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code}")

    data = response.json()
    post_data = data[0]['data']['children'][0]['data']
    return interroger_llm(post_data["title"] + "\n" + post_data["selftext"])

dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_pickle = os.path.join(dossier_script, 'topics.pkl')
chemin_ret = os.path.join(dossier_script, 'topics_classified.pkl')
try:
    with open(chemin_ret, 'rb') as file:
        data = pickle.load(file)
except:
    with open(chemin_pickle, 'rb') as file:
        data = pickle.load(file)

client = OpenAI(
    api_key="YOUR KEY",
    base_url="https://api.groq.com/openai/v1"  # Important : redirige vers Groq
)




for i in data.keys():
    for j in range(len(data[i])):
        if "classified" not in data[i][j]:
            print(data[i][j]["url"])
            ret = get_reddit_post_classification(data[i][j]["url"])
            print(ret)
            data[i][j]["classified"] = ret
            with open(chemin_ret, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
exit()

