from typing import Dict, Any

def get_people_search_query_schema() -> Dict[str, Any]:
    """
    Retrieves the OpenSearch mapping schema for the 'people' index.

    This function sends a POST request to the 11x API to get the mapping,
    which defines the structure and fields available for searching people.

    Returns:
        dict: A dictionary indicating the outcome.
              On success: {"status": "success", "results": dict}  (where dict is the schema)
              On error:   {"status": "error"}
    """
    import requests
    import os
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Check if API_KEY is set
    if "API_KEY" not in os.environ or not os.environ["API_KEY"]:
        logger.error("API_KEY environment variable is not set")
        return {"status": "error", "message": "API_KEY environment variable is not set"}

    # Check if API_URL is set
    if "API_URL" not in os.environ or not os.environ["API_URL"]:
        logger.error("API_URL environment variable is not set")
        return {"status": "error", "message": "API_URL environment variable is not set"}
        
    # Get API URL from environment variable
    api_url = os.environ.get('API_URL')
    url = f"{api_url}/rpc/opensearch/get_mapping"
    payload = {"index_name": "people"}

    print(f"Payload: {payload}")
    
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
            logger.info(f"x-11x-request-id: {request_id}")
        else:
            logger.info("x-11x-request-id header not found in response")
            
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        # Return success status with the schema in results
        return {"status": "success", "results": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        # Check if response exists and has headers
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'headers'):
            request_id = e.response.headers.get('x-11x-request-id')
            if request_id:
                logger.info(f"x-11x-request-id: {request_id}")
        # Attempt to return response text even on failure, if available
        error_details = {"error": str(e)}
        if hasattr(e, 'response') and e.response is not None:
            error_details["status_code"] = e.response.status_code
            try:
                # Try to include JSON error details if the response body is JSON
                error_details["details"] = e.response.json()
            except requests.exceptions.JSONDecodeError:
                # Fallback to raw text if not JSON
                error_details["response_text"] = e.response.text
        # Return error status (error_details could be logged instead of returned)
        return {"status": "error"}
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON response: {e}")
        # Include the raw text that failed to parse
        # Return error status
        return {"status": "error"}

# # Example usage (optional, for testing)
# if __name__ == "__main__":
#     print("Getting people search query schema...")
#     response_data = get_people_search_query_schema()
#     import json
#     print(f"Status: {response_data['status']}")
#     if response_data['status'] == 'success':
#         print("Schema:")
#         print(json.dumps(response_data.get('results'), indent=2))
#     else:
#         print("An error occurred retrieving the schema.")
