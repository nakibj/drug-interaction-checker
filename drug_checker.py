import requests

def search_drug(drug_name):
    response = requests.get(f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:\"{drug_name}\"&limit=1")

    #success!
    if response.status_code == 200:
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            drug_data = data['results'][0]

            generic_name = (drug_data['openfda']['generic_name'])[0]
            interactions = ' '.join(drug_data['drug_interactions'])

            return{
                'generic_name': generic_name,
                'drug_interactions': interactions
            }
    else:
        response = requests.get(f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:\"{drug_name}\"&limit=1")

        #success!
        if response.status_code == 200:
            data = response.json()

            if 'results' in data and len(data['results']) > 0:
                drug_data = data['results'][0]

                generic_name = (drug_data['openfda']['generic_name'])[0]
                interactions = ' '.join(drug_data['drug_interactions'])

                return{
                    'generic_name': generic_name,
                    'drug_interactions': interactions
                }
        
    return None


def check_interactions(drug_a, drug_b):

    results_a = search_drug(drug_a)
    results_b = search_drug(drug_b)


    if results_a is None or  results_b is None:
        return {'error': 'One or both drugs not found'}
    

    final_interactions = {
        'drug_a':{
            'name':results_a['generic_name'],
            'interactions': results_a['drug_interactions']
        },
        'drug_b':{
            'name':results_b['generic_name'],
            'interactions': results_b['drug_interactions']
        }
    }
    
    #Is B mentioned in A interactions?
    drug_b_first_word = results_b['generic_name'].split()[0].lower()
    if drug_b_first_word in results_a['drug_interactions'].lower():
        final_interactions['drug_a']['mentions_drug_b'] = True
    else:
        final_interactions['drug_a']['mentions_drug_b'] = False


    #Is A mentioned in B interactions?
    drug_a_first_word = results_a['generic_name'].split()[0].lower()
    if drug_a_first_word in results_b['drug_interactions'].lower():
        final_interactions['drug_b']['mentions_drug_a'] = True
    else:
        final_interactions['drug_b']['mentions_drug_a'] = False


    
    #Found interactions?
    if final_interactions['drug_a']['mentions_drug_b'] or final_interactions['drug_b']['mentions_drug_a']:
        final_interactions['interaction_found'] = True
    else:
        final_interactions['interaction_found'] = False




    return final_interactions




