import pandas as pd

df = pd.read_csv('rezultate_scraping.csv')
total_sites = len(df)
crawled_successfully = (df['status'] == 'ok').sum()
with_phones = (df['phone_numbers'].str.len() > 0).sum()
with_social = (df['social_links'].str.len() > 0).sum()

print(f"--- ANALIZĂ DATE ---")
print(f"Coverage: {(crawled_successfully / total_sites) * 100:.2f}%")
print(f"Fill Rate Telefoane: {(with_phones / crawled_successfully) * 100:.2f}%")
print(f"Fill Rate Social Media: {(with_social / crawled_successfully) * 100:.2f}%")