from typing import Dict, Any, Optional

def get_people_search_query_results_count(query_json: str) -> Dict[str, Any]:
    """
    Retrieves the count of people matching a specific search query.

    Args:
        query_json (str): A JSON string representing the OpenSearch query.

            Example:
            '{
                "bool": {
                    "must_not": [{"bool": {"should": [{"match_phrase": {"job_title": {"text": "generalist"}}}, {"match_phrase": {"job_title": {"text": "specialist"}}}, {"match_phrase": {"job_title": {"text": "recruiter"}}}]}}],
                    "must": [{"bool": {"should": [{"match_phrase": {"job_title": {"text": "hr"}}}, {"match_phrase": {"job_title": {"text": "human resources"}}}, {"match_phrase": {"job_title": {"text": "operations"}}}, {"match_phrase": {"job_title": {"text": "ta"}}}, {"match_phrase": {"job_title": {"text": "talent acquisition"}}}, {"match_phrase": {"job_title": {"text": "compliance"}}}, {"match_phrase": {"job_title": {"text": "risk management"}}}, {"match_phrase": {"job_title": {"text": "dei"}}}]}}, {"terms": {"job_title_levels": ["senior", "manager", "director", "vp", "partner"]}}, {"terms": {"job_company_news": {"category": ["acquires", "expands_facilities", "expands_offices_in", "expands_offices_to", "increases_headcount_by", "opens_new_location"]}}}, {"term": {"emails": {"type": "current_professional"}}}]
                }
            }'

    This function parses the JSON string, then sends a POST request to the 11x API's
    count endpoint using the parsed query payload.

    Returns:
        dict: A dictionary indicating the outcome.
              On success: {"status": "success", "results": {"count": int}}
              On error:   {"status": "error"}
    """
    import requests
    import os
    import json
    import datetime

    # Check if API_KEY is set
    if "API_KEY" not in os.environ or not os.environ["API_KEY"]:
        print(f"{datetime.datetime.now()} - ERROR - API_KEY environment variable is not set")
        return {"status": "error", "message": "API_KEY environment variable is not set"}

    try:
        query = json.loads(query_json)
    except json.JSONDecodeError as e:
        print(f"{datetime.datetime.now()} - ERROR - Failed to parse query JSON: {e}")
        return {"status": "error", "message": f"Invalid JSON format: {e}"}

    # Check if API_URL is set
    if "API_URL" not in os.environ or not os.environ["API_URL"]:
        print(f"{datetime.datetime.now()} - ERROR - API_URL environment variable is not set")
        return {"status": "error", "message": "API_URL environment variable is not set"}
        
    # Get API URL from environment variable
    api_url = os.environ.get('API_URL')
    url = f"{api_url}/rpc/opensearch/search_people_count"
    
    # Construct the payload using the provided query
    payload: Dict[str, Any] = {"q": query}

    print(f"{datetime.datetime.now()} - INFO - Payload: {payload}")

    # Get API key from environment variable, fall back to empty string if not available
    api_key = os.environ.get('API_KEY', "")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the request ID header if present
        request_id = response.headers.get('x-11x-request-id')
        if request_id:
            print(f"{datetime.datetime.now()} - INFO - x-11x-request-id: {request_id}")
        else:
            print(f"{datetime.datetime.now()} - INFO - x-11x-request-id header not found in response")
            
        response.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)
        # The count endpoint likely returns a simple JSON like {"total": 123}
        result = response.json()
        if isinstance(result, dict) and "total" in result and isinstance(result["total"], int):
            # Return success status with count in results
            return {"status": "success", "results": {"count": result["total"]}}
        else:
            print(f"{datetime.datetime.now()} - ERROR - Unexpected response format: {result}")
            # Return error status due to unexpected format
            return {"status": "error"}
    except requests.exceptions.RequestException as e:
        print(f"{datetime.datetime.now()} - ERROR - HTTP Request failed: {e}")
        # Check if response exists and has headers
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'headers'):
            request_id = e.response.headers.get('x-11x-request-id')
            if request_id:
                print(f"{datetime.datetime.now()} - INFO - x-11x-request-id: {request_id}")
        # Return error status
        return {"status": "error"}
    except requests.exceptions.JSONDecodeError as e:
        print(f"{datetime.datetime.now()} - ERROR - Failed to decode JSON response: {e}")
        # Ensure response is defined before accessing .text
        response_text = response.text if 'response' in locals() and hasattr(response, 'text') else 'No response object or text'
        print(f"{datetime.datetime.now()} - ERROR - Response text: {response_text}")
        # Return error status
        return {"status": "error"}

# # Example usage (optional, for testing)
# if __name__ == "__main__":
#     print("Getting people search query results count...")
#     # Define a sample query as a JSON string
#     sample_query_json = """
#     {
#         "bool": {"should": [{"match": {"job_title": "software engineer"}}]}
#     }
#     """
#     response_data = get_people_search_query_results_count(query_json=sample_query_json)
#     import json
#     print(f"Status: {response_data['status']}")
#     if response_data['status'] == 'success':
#         print("Count:")
#         print(json.dumps(response_data.get('results'), indent=2))
#     elif 'message' in response_data:
#         print(f"Error: {response_data['message']}")
#     else:
#         print("An error occurred during the count retrieval.")
