import streamlit as st

from app import fetch_data

############################################################

def get_data_from_linkedin(email):
    company_data, person_data = fetch_data(email)
        
    result = ""
    if company_data:
        profile = company_data.get('profile', {})
        result += "\n########## Empresa #################"
        result += "\n\nNome: " + (profile.get('name') or "Não disponível")
        result += "\n\nWebsite: " + (profile.get('website') or "Não disponível")
        result += "\n\nLinkedIn: " + (company_data.get('url') or "Não disponível")
        result += "\n\nÁrea de atuação: " + (profile.get('industry') or "Não disponível")
        
        company_size = ", ".join(str(size) for size in profile.get('company_size', [])) if isinstance(profile.get('company_size'), list) else (profile.get('company_size') or "Não disponível")
        company_size_on_linkedin = str(profile.get('company_size_on_linkedin')) or "Não disponível"
        result += "\n\nPorte: " + company_size + " (" + company_size_on_linkedin + " no LinkedIn)"
        
        locations = profile.get('locations', [])
        if locations and isinstance(locations, list) and len(locations) > 0:
            first_location = locations[0]  
            city = first_location.get('city') or "Não disponível"
            state = first_location.get('state') or "Não disponível"
        else:
            city = "Não disponível"
            state = "Não disponível"
        result += "\n\nLocalização: " + city + ", " + state

    if person_data:
        profile = person_data.get('profile', {})
        result += "\n\n\n########## Profissional #################"
        result += "\n\nNome: " + (profile.get('full_name') or "Não disponível")
        result += "\n\nLinkedIn: " + (person_data.get('url') or "Não disponível")
        result += "\n\nCargo: " + (profile.get('occupation') or "Não disponível")
        result += "\n\nLocalização: " + (profile.get('city') or "Não disponível") + ", " + (profile.get('state') or "Não disponível")

    return result


############################################################

st.title("Consulta de perfil via LinkedIn")

with st.form(key='chat_form'):
    user_input = st.text_input("Informe o e-mail aqui:")
    submit_button = st.form_submit_button(label='Submeter')

if submit_button and user_input:
    response = get_data_from_linkedin(user_input)
    st.markdown(response, unsafe_allow_html=True)
