import requests
import time
from datetime import datetime, timedelta, timezone
import pickle
import os

def get_topics(subreddit):
    base_url = f"https://www.reddit.com/r/{subreddit}/new.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    topics = []
    while True:
        url = f"{base_url}?limit=100"
        if 'after' in locals():
            url += f"&after={after}"
        response = requests.get(url, headers=headers)
    
        cnt = 0
        while response.status_code == 429:
            time.sleep(60)
            print("429")
            response = requests.get(url, headers=headers)
            cnt += 1
            if 10 < cnt:
                return topics

        data = response.json()
        posts = data["data"]["children"]

        if not posts:
            return topics  # Plus de posts à parcourir

        for post in posts:
            post_data = post["data"]
            created_utc = datetime.fromtimestamp(post_data["created_utc"], tz=timezone.utc)
            topics.append({"title": post_data["title"],"created": created_utc.strftime("%Y-%m-%d %H:%M:%S"),"url": f"https://reddit.com{post_data['permalink']}"})
   
        # Préparation pagination
        after = data["data"].get("after")
        if not after or 99 < len(topics):
            return topics
        time.sleep(1)  # Respect Reddit rate-limit


subreddit = ["TodayILearned", "NoStupidQuestions","TooAfraidToAsk","ChangeMyView","AskReddit","DoesAnybodyElse","conspiracy","aliens","MandelaEffect","FlatEarth","Paranormal","AlternativeHealth","Nootropics","Skeptic","ThatHappened","thathappenedtoome","PointlessStories","okbuddyretard","AskScienceDiscussion","ExplainLikeImFive"]
pkl_ret = {}

for i in subreddit:
    print(i)
    topics = get_topics(i)
    pkl_ret[i] = topics
    print(len(topics))
    time.sleep(1)


dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_pickle = os.path.join(dossier_script, 'topics.pkl')

with open(chemin_pickle , 'wb') as handle:
    pickle.dump(pkl_ret, handle, protocol=pickle.HIGHEST_PROTOCOL)