import os
import django
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quote.settings')
django.setup()

from quoteapp.models import Author, Quote, Tag

client = MongoClient(
    "mongodb+srv://yvasilishina:vasilishina@cluster0.cupgp4c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = client['quotes_db']

mongo_authors = mongo_db['author']
mongo_quotes = mongo_db['quote']
print("Starting migration...")
mongo_author_id_map = {}

authors_count = mongo_authors.count_documents({})
print(f"Found {authors_count} authors in MongoDB")

for doc in mongo_authors.find():
    author, created = Author.objects.get_or_create(
        fullname=doc['fullname'],
        defaults={
            'born_date': doc.get('born_date', ''),
            'born_location': doc.get('born_location', ''),
            'description': doc.get('description', '')
        }
    )
    mongo_author_id_map[str(doc['_id'])] = author
    print(f"{'Created' if created else 'Found'} author: {author.fullname}")
for doc in mongo_quotes.find():
    author_ref = mongo_author_id_map.get(str(doc['author']))
    if not author_ref:
        continue

    quote_obj = Quote.objects.create(
        quote=doc['quote'],
        author=author_ref
    )

    for tag_name in doc.get('tags', []):
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        quote_obj.tags.add(tag)
