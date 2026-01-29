# Technical Documentation: Data Extraction & Matching API

## 1. Web Scraping Phase (Part 1)
**Goal:** Extract phone numbers and social media links from a list of domains within a 10-minute time constraint.

* **Technology Stack:** Python 3 using `httpx` for asynchronous requests and `BeautifulSoup4` for HTML parsing.
* **Performance Optimization:** To meet the strict 10-minute deadline, I implemented **concurrency control** using `asyncio.Semaphore`. This allowed the script to process multiple websites simultaneously without overwhelming network resources or triggering local timeouts.
* **Extraction Strategy:**
    * **Phone Numbers:** Utilized a specialized Regex for US formats (e.g., `(XXX) XXX-XXXX`), searching both visible page text and `tel:` metadata attributes.
    * **Protocol Fallback:** Implemented a retry logic that automatically attempts `https://` followed by `http://` to maximize the "Coverage" rate for older or misconfigured websites.



## 2. Data Integration & Storage (Part 2.1)
* **Data Merging:** Used the `pandas` library to perform a "left join" between the scraped results and the official company names dataset, using the website URL as the unique primary key.
* **Search Engine Technology:** Selected **Elasticsearch** for storage. Its inverted index structure is specifically designed for high-speed retrieval and complex "Fuzzy Matching" requirements.

## 3. Matching Algorithm & REST API (Part 2.2)
* **Framework:** Built with **FastAPI**, providing a high-performance interface with automated Swagger documentation.
* **Matching Logic:**
    * The API accepts `name`, `phone`, or `website` as inputs.
    * **Fuzzy Search:** Configured Elasticsearch with `fuzziness: "AUTO"`. This allows the system to identify companies even if the user provides partial names or minor typos.
    * **Weighted Scoring:** Implemented field boosting (e.g., `company_name^3`) to ensure that name matches have a higher priority in determining the "best matching" profile.



## 4. Performance Results & Metrics
Based on the execution against the provided datasets, the following results were achieved:

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Total Processing Time** | **< 10 Minutes** | Successfully met the scaling requirement. |
| **Website Coverage** | **11%** | Percentage of websites crawled successfully. |
| **Fill Rate** | **[Insert your calculated %]** | Percentage of crawled sites with extracted data. |
| **Match Rate** | **High** | Efficiency of returning the correct profile from 1,000 entries. |

---

## 5. How to Run the Project
1.  **Start Elasticsearch:** Ensure your local instance is running at `http://localhost:9200`.
2.  **Install Dependencies:** `pip install httpx beautifulsoup4 pandas elasticsearch fastapi uvicorn`
3.  **Index the Data:** Run the indexing script to load the merged CSV into Elasticsearch.
4.  **Start the API:** `uvicorn api:app --reload`
5.  **Test the Endpoint:** Open `http://127.0.0.1:8000/docs` to test the `/match-company` endpoint.