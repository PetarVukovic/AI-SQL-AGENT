def get_query(list_of_dicts,input_str):
    for d in list_of_dicts:
        if d["input"] == input_str:
            return d["query"]
    return None  # Return None if input is not found