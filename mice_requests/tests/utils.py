from bs4 import BeautifulSoup

def get_hidden_input_value(html, name, index=None):
    soup = BeautifulSoup(html, 'html.parser')
    input_tags = soup.find_all('input', {'type': 'hidden', 'name': name})
    
    if index is not None:
        input_tag = input_tags[index]
    else:
        input_tag = input_tags[0]
    
    return input_tag.get('value')