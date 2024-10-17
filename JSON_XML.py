# Example user data
users = [
    {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "email": "ivan.petrov@example.com",
        "phone": "+123456789",
        "profession": "Engineer"
    },
    {
        "first_name": "Anna",
        "last_name": "Ivanova",
        "email": "anna.ivanova@example.com",
        "phone": "+987654321",
        "profession": "Doctor"
    },
    {
        "first_name": "Sergey",
        "last_name": "Sidorov",
        "email": "sergey.sidorov@example.com",
        "phone": "+1122334455",
        "profession": "Teacher"
    }
]

# Function to serialize into JSON format
def serialize_to_json(users):
    json_str = "[\n"
    for user in users:
        json_str += "  {\n"
        json_str += f'    "first_name": "{user["first_name"]}",\n'
        json_str += f'    "last_name": "{user["last_name"]}",\n'
        json_str += f'    "email": "{user["email"]}",\n'
        json_str += f'    "phone": "{user["phone"]}",\n'
        json_str += f'    "profession": "{user["profession"]}"\n'
        json_str += "  },\n"
    json_str = json_str.rstrip(",\n")  # Remove the last comma
    json_str += "\n]"
    return json_str

# Function to serialize into XML format
def serialize_to_xml(users):
    xml_str = "<users>\n"
    for user in users:
        xml_str += "  <user>\n"
        xml_str += f'    <first_name>{user["first_name"]}</first_name>\n'
        xml_str += f'    <last_name>{user["last_name"]}</last_name>\n'
        xml_str += f'    <email>{user["email"]}</email>\n'
        xml_str += f'    <phone>{user["phone"]}</phone>\n'
        xml_str += f'    <profession>{user["profession"]}</profession>\n'
        xml_str += "  </user>\n"
    xml_str += "</users>"
    return xml_str

# Perform serialization to JSON
json_output = serialize_to_json(users)
print("JSON Output:")
print(json_output)

# Perform serialization to XML
xml_output = serialize_to_xml(users)
print("\nXML Output:")
print(xml_output)
