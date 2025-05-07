from typing import Dict, Any, Optional

def validate_people_search_query(query: str) -> Dict[str, Any]:
    """
    Validates a people search query by checking its syntax and structure.

    Args:
        query (str): The search query to validate.

    This function sends a POST request to the 11x API's validate_search_query 
    endpoint with the provided query and hardcoded "people" index name.

    Returns:
        dict: A dictionary indicating the outcome.
              On success: {"status": "success", "results": {validation_results}}
              On error:   {"status": "error", "message": "error_message"}
    """
    import requests
    import os
    import json
    import datetime

    # Check if API_KEY is set
    if "API_KEY" not in os.environ or not os.environ["API_KEY"]:
        print(f"{datetime.datetime.now()} - ERROR - API_KEY environment variable is not set")
        return {"status": "error", "message": "API_KEY environment variable is not set"}

    # Check if API_URL is set
    if "API_URL" not in os.environ or not os.environ["API_URL"]:
        print(f"{datetime.datetime.now()} - ERROR - API_URL environment variable is not set")
        return {"status": "error", "message": "API_URL environment variable is not set"}
        
    # Get API URL from environment variable
    api_url = os.environ.get('API_URL')
    url = f"{api_url}/rpc/opensearch/validate_search_query"
    
    # Construct the payload with the query and hardcoded index_name
    payload = {
        "q": query,
        "index_name": "people"
    }

    print(f"{datetime.datetime.now()} - INFO - Payload: {payload}")

    # Get API key from environment variable
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
            
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
        
        result = response.json()
        return {"status": "success", "results": result}
        
    except requests.exceptions.RequestException as e:
        print(f"{datetime.datetime.now()} - ERROR - HTTP Request failed: {e}")
        # Check if response exists and has headers
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'headers'):
            request_id = e.response.headers.get('x-11x-request-id')
            if request_id:
                print(f"{datetime.datetime.now()} - INFO - x-11x-request-id: {request_id}")
        
        error_message = str(e)
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            try:
                error_data = json.loads(e.response.text)
                if isinstance(error_data, dict) and 'message' in error_data:
                    error_message = error_data['message']
            except json.JSONDecodeError:
                pass
                
        return {"status": "error", "message": error_message}
        
    except json.JSONDecodeError as e:
        print(f"{datetime.datetime.now()} - ERROR - Failed to decode JSON response: {e}")
        response_text = response.text if 'response' in locals() and hasattr(response, 'text') else 'No response object or text'
        print(f"{datetime.datetime.now()} - ERROR - Response text: {response_text}")
        return {"status": "error", "message": f"Failed to decode JSON response: {e}"}

# Example usage (commented out, for testing purposes only)
# if __name__ == "__main__":
#     test_query = "job_title:engineer"
#     result = validate_people_search_query(test_query)
#     print(result)
