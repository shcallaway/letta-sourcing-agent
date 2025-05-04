from typing import Dict, Any


def execute_people_search_query(query_json: str) -> Dict[str, Any]:
    """
    Executes a people search query against the 11x API.

    Args:
        query_json (str): A JSON string representing the OpenSearch query.

            Example:
            '{
                "bool": {
                    "must_not": [{"bool": {"should": [{"match_phrase": {"job_title": {"text": "generalist"}}}, {"match_phrase": {"job_title": {"text": "specialist"}}}, {"match_phrase": {"job_title": {"text": "recruiter"}}}]}}],
                    "must": [{"bool": {"should": [{"match_phrase": {"job_title": {"text": "hr"}}}, {"match_phrase": {"job_title": {"text": "human resources"}}}, {"match_phrase": {"job_title": {"text": "operations"}}}, {"match_phrase": {"job_title": {"text": "ta"}}}, {"match_phrase": {"job_title": {"text": "talent acquisition"}}}, {"match_phrase": {"job_title": {"text": "compliance"}}}, {"match_phrase": {"job_title": {"text": "risk management"}}}, {"match_phrase": {"job_title": {"text": "dei"}}}]}}, {"terms": {"job_title_levels": ["senior", "manager", "director", "vp", "partner"]}}, {"terms": {"job_company_news": {"category": ["acquires", "expands_facilities", "expands_offices_in", "expands_offices_to", "increases_headcount_by", "opens_new_location"]}}}, {"term": {"emails": {"type": "current_professional"}}}]
                }
            }'

    Returns:
        dict: A dictionary indicating the outcome.
              On success: {"status": "success", "results": Dict[str, Any]}
              On error:   {"status": "error"}
    """
    import json
    import os
    import requests
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Check if API_KEY is set
    if "API_KEY" not in os.environ or not os.environ["API_KEY"]:
        logger.error("API_KEY environment variable is not set")
        return {"status": "error", "message": "API_KEY environment variable is not set"}

    # Parse the JSON string into a dictionary
    try:
        query = json.loads(query_json)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse query JSON: {e}")
        return {"status": "error", "message": "Invalid JSON query provided."}

    # Check if API_URL is set
    if "API_URL" not in os.environ or not os.environ["API_URL"]:
        logger.error("API_URL environment variable is not set")
        return {"status": "error", "message": "API_URL environment variable is not set"}
        
    # Get API URL from environment variable
    api_url = os.environ.get('API_URL')
    url = f"{api_url}/rpc/opensearch/search_people"
    
    # Get API key from environment variable, fall back to empty string if not available
    api_key = os.environ.get('API_KEY', "")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # TODO: Add size to the payload
    payload: Dict[str, Any] = {"q": query }

    print(f"Payload: {payload}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the request ID header if present
        request_id = response.headers.get('x-11x-request-id')
        if request_id:
            logger.info(f"x-11x-request-id: {request_id}")
        else:
            logger.info("x-11x-request-id header not found in response")
            
        response.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)

        # Attempt to parse JSON response
        try:
            results = response.json()
            return {"status": "success", "results": results}
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            # Return simple error status
            return {"status": "error"}

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        # Check if response exists and has headers
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'headers'):
            request_id = e.response.headers.get('x-11x-request-id')
            if request_id:
                logger.info(f"x-11x-request-id: {request_id}")
        # Return simple error status
        return {"status": "error"}

# Example usage (optional, for testing)
if __name__ == "__main__":
    print("Executing people search query...")
    # Define a sample query as a JSON string
    sample_query_json = """
    {
        "bool": {"should": [{"match": {"job_title": "software engineer"}}]}
    }
    """
    response_data = execute_people_search_query(query_json=sample_query_json) # Pass the JSON string
    import json
    print(f"Status: {response_data['status']}")
    if response_data['status'] == 'success':
        print("Results:")
        print(json.dumps(response_data.get('results'), indent=2))
    else:
        print("An error occurred during the search.")
