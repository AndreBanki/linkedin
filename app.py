import os
import requests
import json
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

def is_corporate_domain(email):
    # Lista de domínios genéricos que não são corporativos
    generic_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com']
    domain = email.split('@')[-1]
    return domain not in generic_domains

def request_linkedIn(url, params):
    api_key = os.getenv("PROXYCURL_API_KEY")     
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None    

# Função para buscar dados da empresa usando a Proxycurl API
def lookup_company(email):
    domain = email.split('@')[-1]
    url = f'https://nubela.co/proxycurl/api/linkedin/company/resolve'
    params = {
        'company_domain': domain,
        'enrich_profile': 'enrich',
    }
    return request_linkedIn(url, params)

def employee_count(company_url):
    url = f'https://nubela.co/proxycurl/api/linkedin/company/employees/count'
    params = {
        'url': company_url,
        'coy_name_match': 'include',
        'employment_status': 'current',
        'linkedin_employee_count': 'include',
    }
    return request_linkedIn(url, params)
    
def lookup_person(email):
    domain = email.split('@')[-1]

    local_part = email.split('@')[0]    
    if '.' in local_part:
        first_name = local_part.split('.')[0]  # Extrai o primeiro nome antes do ponto
    else:
        first_name = local_part

    url = f'https://nubela.co/proxycurl/api/linkedin/profile/resolve'
    params = {
        'company_domain': domain,
        'first_name': first_name,
        'enrich_profile': 'enrich',
    }
    return request_linkedIn(url, params)

def get_person_data(person_url):
    url = f'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        'linkedin_profile_url': person_url,
        'extra': 'include',
        'github_profile_id': 'include',
        'facebook_profile_id': 'include',
        'twitter_profile_id': 'include',
        'personal_contact_number': 'include',
        'personal_email': 'include',
        'inferred_salary': 'include',
        'skills': 'include',
        'use_cache': 'if-recent', # Costs an extra 1 credit on top of the cost of the base endpoint
        'fallback_to_cache': 'on-error',
    }
    return request_linkedIn(url, params)

# Função principal
def fetch_data(email):
    if not is_corporate_domain(email):
        return None, None, None

    company_data = lookup_company(email)
    person_data = lookup_person(email)

    return company_data, person_data      

def main():  
    email = input("Informe o e-mail: ")

    company_data, person_data = fetch_data(email)

    if company_data:
        print("Dados da Empresa Encontrados:")
        print(company_data)

        json_object = json.dumps(company_data, indent=4)
        with open(f"{email}_company.json", "w") as outfile:
            outfile.write(json_object)
    else:
        print("Nenhuma empresa encontrada para este domínio.")

    if person_data:
        print("Dados do profissional encontrados:")
        print(person_data)
        json_object = json.dumps(person_data, indent=4)
        with open(f"{email}_person.json", "w") as outfile:
            outfile.write(json_object)
    else:
        print("Nenhum profissional encontrado.")    
  

if __name__ == "__main__":
    main()
