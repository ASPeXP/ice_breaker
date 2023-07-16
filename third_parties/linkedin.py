import os
import requests
from dotenv import load_dotenv

# load_dotenv("../.env")
load_dotenv("./.env")


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    api_key = os.getenv("PROXY_API_KEY")
    header_dic = {"Authorization": "Bearer " + api_key}

    params = {
        "url": linkedin_profile_url,
        "fallback_to_cache": "on-error",
        "use_cache": "if-present",
        "skills": "include",
        "inferred_salary": "include",
        "personal_email": "include",
        "personal_contact_number": "include",
        "twitter_profile_id": "include",
        "facebook_profile_id": "include",
        "github_profile_id": "include",
        "extra": "include",
    }

    response = requests.get(api_endpoint, params=params, headers=header_dic)

    # response = requests.get(
    #     api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    # )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def scrape_prapath_linkedin_profile():
    api_endpoint = "https://gist.githubusercontent.com/ASPeXP/c3d274cfbd7f8bfa2f8cbd32c6d662c6/raw/ae48a716bb08d5ecd2f09ae202cfcd5408e90a8c/prapath-suayroop.json"

    response_data = requests.get(api_endpoint)

    data = response_data.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
