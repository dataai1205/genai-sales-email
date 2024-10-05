from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
load_dotenv()
client = OpenAI()

class AIEmail(BaseModel):
    subject: str
    body: str
class CadenceEmailTemplate(BaseModel):
    subject: str
    body: str
    condition: str
class AICadence(BaseModel):
    steps: list[CadenceEmailTemplate]
class ReceipientInfo(BaseModel):
    company_name: str
    company_description: str
    industry: str
class ProductInfo(BaseModel):
    company_product_name: str
    customer_pain_points: str
    value_proposition: str
    call_to_actions: str
    company_overview: Optional[str] = None
    additional_context: Optional[str] = None
class SenderInfo(BaseModel):
    sender_name: str

def gen_ai_email(product_info): 
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful email writer."},
            {
                "role": "user",
                "content": f"""Write a email With given these informations.
Product Info: {product_info}
"""
            }
        ],
        temperature=0.7,
        max_tokens=512,
        n=2,
        response_format=AIEmail

    )
    
    email_subject1 = completion.choices[0].message.parsed.subject
    email_body1 = completion.choices[0].message.parsed.body
    email_subject2 = completion.choices[1].message.parsed.subject
    email_body2 = completion.choices[1].message.parsed.body
    return email_subject1, email_subject2, email_body1, email_body2
def gen_ai_cadence(product_info): 
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful optimized cadence designer in sales marketing field."},
            {
                "role": "user",
                "content": f"""Write a optimized cadence with given informations.
Product Info: {product_info}
"""
            }
        ],
        temperature=0.7,
        max_tokens=512,
        response_format=AICadence

    )

    
    ai_cadence = completion.choices[0].message.parsed
    for step in ai_cadence.steps:
        print(step)
    return ai_cadence.steps
    

if __name__ == "__main__":

    recipient_info = ReceipientInfo(
        company_name="Tech Innovations Inc.",
        company_description="A leading company in tech solutions.",
        industry="Technology"
    )
    product_info = ProductInfo(
        company_product_name="AIVIO",
        customer_pain_points="Too much manual work finding prospects and creating personalized outreach",
        value_proposition="End-to-end sales funnel automation",
        call_to_actions="schedule a meeting",
        company_overview="The only data intelligence and sales engagement platform that you'll ever need",
        # additional_context="AIVIO made it easy for me to test different content to land the perfect email message."
    )
    sender_info = SenderInfo(
        sender_name="Andrew"
    )
    # email_subject1, email_subject2, email_body1, email_body2 = gen_ai_email(receipient_info=recipient_info, product_info=product_info, sender_info=sender_info)
    # print(email_subject1)
    # print(email_body1)
    gen_ai_cadence(product_info=product_info)