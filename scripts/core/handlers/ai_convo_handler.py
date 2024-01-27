import hashlib
import json

import vertexai
from vertexai.language_models import TextGenerationModel

from scripts.config import AIConfig
from scripts.core.db.redis_connections import redis_connection

vertexai.init(project=AIConfig.PROJECT, location=AIConfig.REGION)


def get_filter_json(query: str, location: str = None) -> dict:
    hash_key = hashlib.md5(json.dumps({"query": query, "location": location}).encode()).hexdigest()
    if redis_connection.exists(hash_key):
        return json.loads(redis_connection.get(hash_key))
    parameters = {"candidate_count": 1, "max_output_tokens": 1024, "temperature": 0.2, "top_p": 0.8, "top_k": 40}
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        """Generate a JSON matching the following model:

    {
    title: Optional[str],
    sector: Optional[List[str]]
    city: Optional[List[str]]
    state: Optional[List[str]]
    pincode: Optional[List[int]]
    }

    Here all the options in the JSON relate to a job and location of the job.

    The user will be giving input of details of the job and maybe the location.

    If user is providing any country as location, don\'t provide any location context in output.

    If any context goes like having any letter or something provide it as normal input of json.

    If User Location is provided but the context has some other location within India, provide the location context in output.

    If any other context comes give empty json.

    input: Software Engineering jobs in Uttar Pradesh.
    output: {
    \"title\": \"Software Engineer\",
    \"state\": [\"Uttar Pradesh\"]
    }

    input: Jobs near me related to Mechanical.

    User Location: Ahmedabad
    output: {
    \"city\": [\"Ahmedabad\"],
    \"sector\": [\"Mechanical\"]
    }

    input: Software Engineer jobs in India.

    User Location: Odisha
    output: {
    \"title\": \"Software Engineer\"
    }

    input: Can you show me magic?
    output: {
    }

    """
        + f"""input: {query}

        """
        + (f"User Location: {location}" if location else "")
        + """

        output:""",
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    redis_connection.set(hash_key, response.text)
    return json.loads(response.text)
