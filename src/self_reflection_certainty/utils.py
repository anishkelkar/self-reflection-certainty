"""
Utility functions for self-reflection certainty.
"""


def map_response_to_score(response: str) -> float:
    response = response.strip().upper()
    
    if response == "A":
        return 1.0
    elif response == "B":
        return 0.0
    elif response == "C":
        return 0.5
    else:
        # Handle unexpected responses - default to unsure
        return 0.5


def format_result(result: dict) -> str:
    certainty = result['certainty_score']
    trust_level = "High" if certainty >= 0.7 else "Medium" if certainty >= 0.4 else "Low"
    
    return f"""Answer: {result['answer']}
Certainty Score: {certainty:.2f}
Trust Level: {trust_level}
Individual Scores: {result['evaluation_scores']}"""