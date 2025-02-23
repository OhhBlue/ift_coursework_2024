import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from src.data_models.company import Company, ESGReport, SearchResult
from src.esg_reports.search import Search  
from src.esg_reports.validate import SearchResultValidator  

from loguru import logger

def main():
    company = Company(
        symbol="AAPL",
        security="Apple Inc.",
        gics_sector="Technology",
        gics_industry="Technology",
        country="USA",
        region="North America",
    )
    
    search_instance = Search(company=company)
    
    google_results = search_instance.google()
    
    if google_results:
        validator = SearchResultValidator(company=company, search_results=google_results)
        valid_google_results = validator.validated_results
        if valid_google_results:
            google_best = valid_google_results[0]
        else:
            google_best = None
            logger.warning("The search results returned by the Google API did not pass validation.")
    else:
        google_best = None
        logger.warning("The Google API did not return any search results.")
    
    sustainability_result = search_instance.sustainability_reports_dot_com()
    
    print("\n=== ESG report search results ===\n")
    
    if google_best:
        print(f"[Google API] Latest ESG report link: {google_best.link}")
    else:
        print("[Google API] No ESG report link found that meets the criteria.")
    
    if sustainability_result and sustainability_result.url:
        print(f"[SustainabilityReports.com] Latest ESG report link: {sustainability_result.url} (Year: {sustainability_result.year})")
    else:
        print("[SustainabilityReports.com] No valid ESG report link found.")

if __name__ == "__main__":
    main()
