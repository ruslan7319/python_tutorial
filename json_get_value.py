
import requests ,json
from jsonpath_ng.ext import parse

url = "https://cde8bdc4bb9d45de9b1fff00c4118687.api.mockbin.io/"
#json_path ="$[0].Item01.Data[0].Results[0].Contact.Address.PostalCode"
# json_path = "$[0].Item01.Data[0].Results[0].Relevance"
json_path = "$[0].Item01.Data[0].Results[1].Relevance"
json_path_array_list = "$[0].Item01.Data[0].Results"

def get_api_json_response(url):
    try:
        # Send GET request
        response = requests.get(url)
        # Raise an exception for HTTP errors (e.g., 404, 500)
        response.raise_for_status()
        # Return the parsed JSON data
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except ValueError:
        return {"error": "Response is not valid JSON"}


def find_item_jsonpath_expression(json_data, json_path_exp):
    try:
       jsonpath_expression = parse(json_path_exp)
       # Find all matches in the data
       matches = jsonpath_expression.find(json_data)
       match_value = [match.value for match in matches]
       return match_value
    except ValueError:
        return {"error": "Response is not valid JSON or not valid json path expression"}

def count_results_items(data):
    total_count = 0
    for item in data:
        for key in item:
            for data_entry in item[key].get("Data", []):
                # Count the number of elements in the Results list
                total_count += len(data_entry.get("Results", []))
    return total_count


json_string = get_api_json_response(url)
array_count = count_results_items(json_string)
item_in_array = 0
Relevance = []

while item_in_array < array_count:
    json_path = f"$[0].Item01.Data[0].Results[{item_in_array}].Relevance"
    json_result = find_item_jsonpath_expression(json_string, json_path)
    Relevance.append(json_result)
    item_in_array +=1

print(Relevance)


#
# # json_result = find_item_jsonpath_expression( json_string , json_path)
# # print(json_result)
# json_data = str(json_string)
# print(json_data)



# json_data = [{'Item01': {'MetaInfo': {'Timestamp': '2023-02-16T08:15:21.000+0000'}, 'Data': [{'_type': 'SearchResultsContact', 'DataId': 1987, 'Results': [{'Relevance': 0.5, 'Contact': {'Name': 'John Doe', 'Phone': '+1-555-123-4567', 'Email': 'johndoe@email.com', 'Address': {'Street': '123 Main St', 'City': 'Anytown', 'State': 'CA', 'PostalCode': '12345'}, 'Active': True, 'Notes': 'New customer'}}]}]}}]
# print(f"Total Relevance: {count_results_items(json_data)}")


