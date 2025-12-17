from fastapi import FastAPI
import uvicorn
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
from typing import List


app = FastAPI()


class UrlsRequest(BaseModel):
    urls: List[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to the SEO API World."}

@app.post("/seo-check")
def seo_check(request: UrlsRequest):
    issues = []
    for url in request.urls:
      try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
  
        title = soup.title.string if soup.title else None
        title_length = len(title) if title else 0
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc_content = meta_desc.get("content") if meta_desc else None
        desc_length = len(meta_desc_content) if meta_desc_content else 0
        h1 = soup.find("h1")
        h1_tags = soup.find_all("h1")
        robots_tags = soup.find_all("meta", attrs={"name": "robots"})


       

        
        
        url_issues = {}
        if not title:
                url_issues["missing_title"] = "Missing <title> tag."
        elif title_length < 50 or title_length > 60:
                url_issues["title_length"] = f"Title length is {title_length} characters (should be 50-60)."
        if not meta_desc or not meta_desc_content:
                url_issues["missing_description"] = "Missing Description Meta tag."
        elif desc_length < 150 or desc_length > 160:
                url_issues["description_length"] = f"Description length is {desc_length} characters (should be 150-160)."
        if not h1:
                url_issues["missing_h1"] = "Missing H1 tag."
        if len(h1_tags) > 1:
               url_issues["multiple_h1"] = f"Found {len(h1_tags)} - H1 tags (should be only one)."
        if not robots_tags:
                url_issues["missing_robots"] = "Missing Robots meta tag."
        elif len(robots_tags) > 1:
                url_issues["duplicate_robots"] = f"Found {len(robots_tags)} - robots tags (should be only one)."

       
        
        if url_issues:
          issues.append({
            "url": url,
            # "title": title,
            # "meta_description": meta_desc.get("content") if meta_desc else None,
            # "h1": h1.text if h1 else None,
            "issue_types": url_issues
        })
       

      except Exception as e:
          issues.append({
                "url": url,
                "error": str(e)
            })
         
    return { 
        "total_urls": len(request.urls),
        "issues": issues
        }
# To run this app, use the command:
# uvicorn app:app --reload