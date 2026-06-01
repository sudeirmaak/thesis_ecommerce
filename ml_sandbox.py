import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('dataset.csv')
features = ['description', 'tags', 'origin', 'roast_level', 'tasting_notes']

for feature in features:
    df[feature] = df[feature].fillna('')

def create_soup(x):
    return (x['description'] + ' ' + 
            x['tags'] + ' ' + 
            x['origin'] + ' ' + 
            x['roast_level'] + ' ' + 
            x['tasting_notes'])

df['combined_features'] = df.apply(create_soup, axis=1)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['name']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim, top_n=4):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]

        coffee_indices = [i[0] for i in sim_scores]
        scores = [i[1] for i in sim_scores]

        print(f"for {title} recommend: ")
        for i, index in enumerate(coffee_indices):
            match_percentage = round(scores[i] * 100, 2)
            print(f"{i+1}. {df['name'].iloc[index]} ({match_percentage}% Match)")

    except KeyError:
        print("not found in dataset")
        

test_coffee_name = df['name'].iloc[0]
get_recommendations(test_coffee_name) 