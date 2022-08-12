import data

db = data.init_db()
listings = data.get_listings(db)

a = [listing for listing in listings if listing['de']]
print(a)