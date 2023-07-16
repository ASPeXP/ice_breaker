from dotenv import load_dotenv
import os

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agent.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agent.twitter_lookup_agent import lookup as twitter_lookup_agent

from third_parties.linkedin import (
    scrape_linkedin_profile,
    scrape_prapath_linkedin_profile,
)
from third_parties.twitter import (
    scrape_user_tweets,
)

from output_parser import person_intel_parser, PersonIntel

load_dotenv("./.env")

# information = """
#     Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a business magnate and investor. He is the founder, CEO, and chief engineer of SpaceX; angel investor, CEO, and product architect of Tesla, Inc.; founder, owner, CTO, and chairman of X Corp.; founder of the Boring Company; co-founder of Neuralink and OpenAI; and president of the philanthropic Musk Foundation. Musk is the wealthiest person in the world, with an estimated net worth as of July 2, 2023, of around US$234 billion according to the Bloomberg Billionaires Index and $238 billion according to Forbes's Real Time Billionaires list, primarily from his ownership stakes in Tesla and SpaceX.[4][5][6]

# Musk was born in Pretoria, South Africa, and briefly attended the University of Pretoria before moving to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University and transferred to the University of Pennsylvania, where he received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University. After two days, he dropped out and, with his brother Kimbal, co-founded the online city guide software company Zip2. Zip2 was acquired by Compaq for $307 million in 1999, and with $12 million of the money he made, that same year Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal.

# In 2002, eBay acquired PayPal for $1.5 billion, and that same year, with $100 million of the money he made, Musk founded SpaceX, a spaceflight services company. In 2004, he was an early investor in the electric vehicle manufacturer Tesla Motors, Inc. (now Tesla, Inc.). He became its chairman and product architect, assuming the position of CEO in 2008. In 2006, he helped create SolarCity, a solar energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, Musk proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year, he co-founded Neuralink—a neurotechnology company developing brain–computer interfaces—and the Boring Company, a tunnel construction company. In 2022, his acquisition of Twitter for $44 billion was completed.

# Musk has expressed views that have made him a polarizing figure. He has been criticized for making unscientific and misleading statements, including that of spreading COVID-19 misinformation. In 2018, the U.S. Securities and Exchange Commission (SEC) sued Musk for falsely tweeting that he had secured funding for a private takeover of Tesla. To settle the case, Musk stepped down as chairman of Tesla and paid a $20 million fine.
# """
# information = """
#     Prapath has background more than 10 years expertise in web development in ASP.Net (Classic) with SQL server database 
#     but today he is  is Software developer, Teacher and Solo Entrepreneur through API developer with Python Flask, 
#     Python Django, PHP, ReactJS and more than 4 years in operation support in EMS, 3.5 years mPOS business 
#     and 2.7 years in enterprise retail POS in Thailand. Also with his interesting in Cloud technology with Amazon EC2,  
#     Microsoft Azure and digital ocean 2. Python language, Go lang, Ruby on rails API and ReactJS. 
#     Container with docker and kubernetes. 
# """
name = "Prapath Suayroop"
# name = "Elon Musk"


def ice_break(name: str) -> PersonIntel:
    # print(os.getenv('OPENAI_API_KEY'))
    # print(os.getenv('PROXY_API_KEY'))
    linkedin_profile_url = linkedin_lookup_agent(name="Elon musk")

    # tweets = scrape_user_tweets(username="@elonmusk", num_tweets=100)
    # print(tweets)
    tweeter_username = twitter_lookup_agent(name="Elon musk")
    # print(tweeter_username)
    # return tweeter_username

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        3. A topic that may interest them
        4. 2 creative Ice breakers to open a conversation with them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # linkedin_data = scrape_linkedin_profile("https://www.linkedin.com/in/prapaths/")

    # # linkedin_data = scrape_linkedin_profile(
    # #     linkedin_profile_url = linkedin_profile_url

    # # )
    linkedin_data = scrape_prapath_linkedin_profile()

    # # print(linkedin_data)
    result = chain.run(information=linkedin_data)
    # print(result)
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")
    # return result


if __name__ == "__main__":
    print("Hello Langchain")
    result = ice_break(name=name)
