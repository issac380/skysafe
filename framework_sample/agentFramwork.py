from typing import Dict, List
from autogen import ConversableAgent
import sys
import os
import numpy as np
import json
import re

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    # TODO
    # INPUT: Restuarant Name and the entire Review Dataset
    # OUTPUT: List containing only the reviews with the restuarant name
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call. 
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}
    print("Parsing review file for: ", restaurant_name)
    with open("restaurant-data.txt", "r") as f:
        data = f.readlines()

    restaurant_name = re.sub(r'[^a-zA-Z0-9]', '', restaurant_name).lower()

    relevant_reviews = []
    for line in data:
       restuarant_name_from_review, review_content = line.strip().split(".", 1)
       if restuarant_name_from_review and review_content:
           if re.sub(r'[^a-zA-Z0-9]', '', restuarant_name_from_review).lower() == restaurant_name:
               relevant_reviews.append(review_content)

    print("Found ", len(relevant_reviews), " reviews for ", restaurant_name)
    return {restaurant_name: relevant_reviews}

def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    # TODO
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
    total_score = 0
    for i in range(len(food_scores)):
        total_score += np.sqrt(food_scores[i]**2 * customer_service_scores[i])
    return total_score * 10 / (len(food_scores) * np.sqrt(125))

    
def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    # TODO
    # It may help to organize messages/prompts within a function which returns a string. 
    # For example, you could use this function to return a prompt for the data fetch agent 
    # to use to fetch reviews for a specific restaurant.
    prompt = f"""
    You are an assistant that can fetch reviews for a specific restaurant.
    You will be given a query, in which the user requests information about a restaurant.
    You need to identify the name of the restaurant being queried.
    
    Please respond with a function call to fetch_restaurant_data with the restaurant name.
    Query: {restaurant_query}
    """
    return prompt

def get_review_analysis_agent_prompt() -> str:
    prompt = """
    You are an assistant that can analyze reviews for a specific restaurant.
    You will be given a list of reviews for a restaurant, and you need to analyze the reviews to extract a food score, and a customer service score based on keywords.
    Here are the keywords the agent should look out for:
    Score 1/5 has one of these adjectives: awful, horrible, or disgusting.
    Score 2/5 has one of these adjectives: bad, unpleasant, or offensive.
    Score 3/5 has one of these adjectives: average, uninspiring, or forgettable.
    Score 4/5 has one of these adjectives: good, enjoyable, or satisfying.
    Score 5/5 has one of these adjectives: awesome, incredible, or amazing.
    Each review will have exactly only two of these scores. 
    You need to analyze the reviews to extract the two scores.

    Please parse each review and respond with a list of python lists with the following format:
    {
        "food_score": [list of all food scores],
        "customer_service_score": [list of all customer service scores]
    }
    Please DO NOT include any other characters in your response.
    """
    return prompt

def get_score_aggregation_agent_prompt() -> str:
    prompt = f"""
    You are an assistant that can aggregate scores for a specific restaurant.
    You will be given a restaurant name, and a list of food scores, and a list of customer service scores.
    
    Please respond with a function call to calculate_overall_score with the following parameters:
    1. restaurant_name: a string
    2. food_scores: a list of integers (1-5)
    3. customer_service_scores: a list of integers (1-5)
    Please respond with a function call to calculate_overall_score with the correct arguments.
    """
    return prompt

# Do not modify the signature of the "main" function.
def main(user_query: str):
    entrypoint_agent_system_message = "" # TODO
    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    # the main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=entrypoint_agent_system_message, 
                                        llm_config=llm_config)
    entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    # TODO
    data_fetch_agent = ConversableAgent("data_fetch_agent", 
                                        system_message=get_data_fetch_agent_prompt(user_query), 
                                        llm_config=llm_config)
    data_fetch_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    data_fetch_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    review_analysis_agent = ConversableAgent("review_analysis_agent", 
                                        system_message=get_review_analysis_agent_prompt(), 
                                        llm_config=llm_config)
    #review_analysis_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    #review_analysis_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    score_aggregation_agent = ConversableAgent("score_aggregation_agent", 
                                        system_message=get_score_aggregation_agent_prompt(), 
                                        llm_config=llm_config)
    score_aggregation_agent.register_for_llm(name="calculate_overall_score", description="Calculates the overall score for a restaurant.")(calculate_overall_score)
    score_aggregation_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)
    
    data_fetched = data_fetch_agent.generate_reply(messages=[{"content": user_query, "role": "user"}])
    function_call = data_fetched['tool_calls'][0]['function']['arguments']
    restaurant_data = fetch_restaurant_data(function_call.split('"')[3])
    restaurant_name = list(restaurant_data.keys())[0]
    reviews = restaurant_data[restaurant_name]
    #print(data_fetched)

    reviews_content = "\n".join(reviews)
    review_analysis_result = review_analysis_agent.generate_reply(messages=[{"content": reviews_content, "role": "user"}])
    review_analysis_result = eval(review_analysis_result)
    food_scores, customer_service_scores = review_analysis_result['food_score'], review_analysis_result['customer_service_score']


    score_aggregation_result = score_aggregation_agent.generate_reply(messages=[{"content": f"restuarant name is {restaurant_name}, food scores are {food_scores} and customer service scores are {customer_service_scores}", "role": "user"}])

    function_args = json.loads(score_aggregation_result['tool_calls'][0]['function']['arguments'])
    restuarant_score = calculate_overall_score(function_args['restaurant_name'], function_args['food_scores'], function_args['customer_service_scores'])
    print(restuarant_score)

    
# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])