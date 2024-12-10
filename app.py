import os
import requests
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Função para verificar se o domínio é corporativo
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
        'similarity_checks': 'include',
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
def main():
  
    email = input("Informe o e-mail: ")

    if not is_corporate_domain(email):
        print("Este não é um domínio corporativo.")
        return

    company_data = lookup_company(email)

    if company_data:
        print("Dados da Empresa Encontrados:")
        print(company_data)

        #company_url = company_data['url']
        #employees = employee_count(company_url)
        #print("\n\nColaboradores:")
        #print(employees)
    else:
        print("Nenhuma empresa encontrada para este domínio.")

    person_data = lookup_person(email)

    if person_data:
        print("Dados do profissional encontrados:")
        print(person_data)

        person_url = person_data['url']
        profile = get_person_data(person_url)
        print(profile)
    else:
        print("Nenhum profissional encontrado.")        

if __name__ == "__main__":
    main()
