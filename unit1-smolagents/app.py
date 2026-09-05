import gradio_patch
from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

from dotenv import load_dotenv

load_dotenv()

import whois

@tool
def check_domain_age(domain: str) -> str:
    """Checks how old a domain is, to help spot recently-registered (often suspicious) domains.
    Args:
        domain: The domain name to check, e.g. 'google.com'
    """
    try:
        info = whois.whois(domain)
        creation_date = info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date is None:
            return f"No WHOIS registration date found for {domain} (it may be a subdomain of a larger service, like GitHub Pages or is-a.dev, rather than a traditionally registered domain)."
            
        return f"Domain {domain} was registered on: {creation_date}"
    except Exception as e:
        return f"Could not retrieve WHOIS data for {domain}: {str(e)}"


import requests
import base64
import time
import os

@tool
def check_url_safety(url: str) -> str:
    """Checks whether a URL is flagged as malicious using VirusTotal.
    Args:
        url: The full URL to check, e.g. 'http://example.com'
    """
    
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    headers = {"x-apikey": api_key}

    # Step 1: submit the URL to VirusTotal for scanning
    try:
        submit_response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )
        submit_response.raise_for_status()
        analysis_id = submit_response.json()["data"]["id"]

        # Step 2: wait a moment, then fetch the scan result
        time.sleep(15)
        result = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )
        result.raise_for_status()
        stats = result.json()["data"]["attributes"]["stats"]
        
    except Exception as e:
        return f"Could not complete scan for {url}: {str(e)}"

    verdict = "likely safe" if stats["malicious"] <= 2 else "potentially unsafe"
    return f"Scan result for {url}: {stats['malicious']} malicious, {stats['suspicious']} suspicious, {stats['harmless']} harmless (out of {sum(stats.values())} engines). Verdict: {verdict} (a small number of flags out of many engines is often a false positive)."

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer,check_domain_age,check_url_safety], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()