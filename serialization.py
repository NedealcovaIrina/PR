# Example data for serialization/deserialization
test_data = {
    "user": {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    },
    "numbers": [1, 2, 3, 4],
    "details": {
        "height": 170,
        "weight": 65,
        "preferences": ["music", "reading"]
    }
}

# Custom Serialization Function (from your previous task)
def custom_serialize(data):
    if isinstance(data, dict):
        serialized_str = "D:{"
        for key, value in data.items():
            serialized_str += f"k:{custom_serialize(key)}:v:{custom_serialize(value)};"
        serialized_str = serialized_str.rstrip(";")  # Remove last semicolon
        serialized_str += "}"
        return serialized_str
    elif isinstance(data, list):
        serialized_str = "L:["
        for item in data:
            serialized_str += f"{custom_serialize(item)};"
        serialized_str = serialized_str.rstrip(";")  # Remove last semicolon
        serialized_str += "]"
        return serialized_str
    elif isinstance(data, str):
        return f"str({data})"
    elif isinstance(data, int):
        return f"int({data})"
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")

# Custom Deserialization Function
def custom_deserialize(serialized_str):
    # Helper function to split by ';' but consider nested structures
    def split_items(data, start, end):
        nested_level = 0
        current_part = ""
        result = []
        for char in data[start:end]:
            if char in '{[':
                nested_level += 1
            elif char in '}]':
                nested_level -= 1
            if char == ';' and nested_level == 0:
                result.append(current_part)
                current_part = ""
            else:
                current_part += char
        if current_part:
            result.append(current_part)
        return result

    if serialized_str.startswith("D:{"):
        data_dict = {}
        key_values = split_items(serialized_str, 3, -1)  # Split dictionary content
        for kv in key_values:
            k_str, v_str = kv.split(":v:", 1)
            key = custom_deserialize(k_str[2:])  # Deserialize key
            value = custom_deserialize(v_str)    # Deserialize value
            data_dict[key] = value
        return data_dict

    elif serialized_str.startswith("L:["):
        elements = split_items(serialized_str, 3, -1)  # Split list content
        return [custom_deserialize(element) for element in elements]  # Deserialize each item

    elif serialized_str.startswith("str(") and serialized_str.endswith(")"):
        return serialized_str[4:-1]  # Extract the string content inside 'str(...)'

    elif serialized_str.startswith("int(") and serialized_str.endswith(")"):
        return int(serialized_str[4:-1])  # Convert string inside 'int(...)' to an integer

    else:
        raise ValueError(f"Invalid serialized string: {serialized_str}")

# Perform serialization
serialized_data = custom_serialize(test_data)
print("Serialized Data:")
print(serialized_data)

# Perform deserialization
deserialized_data = custom_deserialize(serialized_data)
print("\nDeserialized Data:")
print(deserialized_data)
