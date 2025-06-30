import json
import re
import json_repair
import os
from ..utils.llm import create_chat_completion
from ..prompts import PromptFamily

async def choose_agent(
    query,
    cfg,
    parent_query=None,
    cost_callback: callable = None,
    headers=None,
    prompt_family: type[PromptFamily] | PromptFamily = PromptFamily,
    **kwargs
):
    """
    Chooses the agent automatically
    Args:
        parent_query: In some cases the research is conducted on a subtopic from the main query.
            The parent query allows the agent to know the main context for better reasoning.
        query: original query
        cfg: Config
        cost_callback: callback for calculating llm costs
        prompt_family: Family of prompts

    Returns:
        agent: Agent name
        agent_role_prompt: Agent role prompt
    """
    query = f"{parent_query} - {query}" if parent_query else f"{query}"
    response = None  # Initialize response to ensure it's defined

    try:
        # Check if we're using a local MLX-like server
        base_url = os.environ.get("OPENAI_BASE_URL", "")
        is_local_server = "localhost" in base_url or "127.0.0.1" in base_url

        if cfg.smart_llm_provider == "openai" and is_local_server:
            # For local servers like MLX, combine system and user messages to avoid issues
            system_content = f"{prompt_family.auto_agent_instructions()}"
            user_content = f"task: {query}"
            combined_content = f"{system_content}\\n\\n{user_content}"
            
            messages = [{"role": "user", "content": combined_content}]
        else:
            # Original format for other providers
            messages=[
                {"role": "system", "content": f"{prompt_family.auto_agent_instructions()}"},
                {"role": "user", "content": f"task: {query}"},
            ]

        response = await create_chat_completion(
            model=cfg.smart_llm_model,
            messages=messages,
            temperature=0.15,
            llm_provider=cfg.smart_llm_provider,
            llm_kwargs=cfg.llm_kwargs,
            cost_callback=cost_callback,
            **kwargs
        )

        agent_dict = json.loads(response)
        return agent_dict["server"], agent_dict["agent_role_prompt"]

    except Exception as e:
        return await handle_json_error(response)


async def handle_json_error(response):
    try:
        agent_dict = json_repair.loads(response)
        if agent_dict.get("server") and agent_dict.get("agent_role_prompt"):
            return agent_dict["server"], agent_dict["agent_role_prompt"]
    except Exception as e:
        print(f"⚠️ Error in reading JSON and failed to repair with json_repair: {e}")
        print(f"⚠️ LLM Response: `{response}`")

    json_string = extract_json_with_regex(response)
    if json_string:
        try:
            json_data = json.loads(json_string)
            return json_data["server"], json_data["agent_role_prompt"]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    print("No JSON found in the string. Falling back to Default Agent.")
    return "Default Agent", (
        "You are an AI critical thinker research assistant. Your sole purpose is to write well written, "
        "critically acclaimed, objective and structured reports on given text."
    )


def extract_json_with_regex(response):
    json_match = re.search(r"{.*?}", response, re.DOTALL)
    if json_match:
        return json_match.group(0)
    return None
