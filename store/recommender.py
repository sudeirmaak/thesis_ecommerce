import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product

def get_recommendations(product_id, top_n=7):
    products = Product.objects.exclude(category__slug='brewing-equipment')

    if products.count() <= 1:
        return []
    
    df = pd.DataFrame(list(products.values('id', 'name', 'description', 'tags', 'origin', 'roast_level', 'tasting_notes')))
    features = ['description', 'tags', 'origin', 'roast_level', 'tasting_notes']

    for feature in features:
        df[feature] = df[feature].fillna('')
        df[feature] = df[feature].astype(str).replace('None', '')

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
    
    try:
        idx = df.index[df['id'] == product_id].tolist()[0]
    except IndexError:
        return []
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    product_indices = [i[0] for i in sim_scores]
    recommended_ids = df['id'].iloc[product_indices].tolist()

    unordered_products = Product.objects.filter(id__in=recommended_ids)
    products_dict = {product.id: product for product in unordered_products}

    recommended_products = [
        products_dict[rid] for rid in recommended_ids if rid in products_dict
    ]

    return recommended_products
