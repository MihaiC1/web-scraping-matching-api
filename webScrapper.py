import asyncio
import httpx
import re
import pandas as pd
from bs4 import BeautifulSoup

# Configurări
CONCURRENT_LIMIT = 20 # Procesăm doar 20 de site-uri simultan (mai sigur pentru conexiuni casnice)
US_PHONE_REGEX = r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9][02-9])\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'

async def scrape_url(client, domain, semaphore):
    async with semaphore: # Aici controlăm fluxul
        domain = domain.strip().lower()
        # Încercăm direct cu HTTPS, apoi HTTP dacă eșuează
        protocols = [f"https://{domain}", f"http://{domain}"]
        
        for url in protocols:
            try:
                response = await client.get(url, timeout=15.0, follow_redirects=True)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Curățăm codul inutil pentru a găsi textul mai ușor
                    for s in soup(["script", "style"]): s.decompose()
                    
                    text = soup.get_text(separator=' ')
                    matches = re.findall(US_PHONE_REGEX, text)
                    phones = [a['href'].split(':')[-1] for a in soup.find_all('a', href=re.compile(r'^tel:'))]
                    # 2. Extrage din textul vizibil
                    text = soup.get_text(separator=' ')
                    matches = re.findall(US_PHONE_REGEX, text)
                    for m in matches:
                        # Reconstruim numărul din grupurile regex
                        clean_num = "".join([g for g in m if g]).strip()
                        if len(re.sub(r'\D', '', clean_num)) >= 10:
                            phones.append(clean_num)

                    # Curățăm lista finală
                    final_phones = list(set([p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]))
                    socials = [a['href'] for a in soup.find_all('a', href=True) 
                              if any(k in a['href'].lower() for k in ['facebook.com', 'linkedin.com', 'instagram.com'])]

                    return {"website": domain, "phone_numbers": "; ".join(final_phones), "social_links": "; ".join(list(set(socials))), "status": "ok"}
            except Exception:
                continue # Trecem la următorul protocol (HTTP) sau finalizăm
                
        return {"website": domain, "phone_numbers": "", "social_links": "", "status": "failed"}

async def main():
    df = pd.read_csv('sample-websites.csv')
    domains = df['domain'].tolist()
    
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    
    # Configurare client ultra-stabilă
    limits = httpx.Limits(max_connections=CONCURRENT_LIMIT, max_keepalive_connections=5)
    timeout = httpx.Timeout(20.0, pool=None) # pool=None înseamnă că așteaptă oricât în coadă fără timeout
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

    async with httpx.AsyncClient(limits=limits, timeout=timeout, headers=headers, verify=False) as client:
        tasks = [scrape_url(client, d, semaphore) for d in domains]
        results = await asyncio.gather(*tasks)
    
    df_out = pd.DataFrame(results)
    df_out.to_csv('rezultate_scraping.csv', index=False)
    print(f"Finalizat! Coverage: {(df_out['status'] == 'ok').sum() / len(domains) * 100:.2f}%")

if __name__ == "__main__":
    asyncio.run(main())