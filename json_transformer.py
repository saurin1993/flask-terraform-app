import json
from datetime import datetime

def transform_value(key, value):
    # Handle 'S' (String) type
    if 'S' in value:
        sanitized_value = value['S'].strip()

        # Check if the string is in RFC3339 format (without regex, using a try-except approach)
        try:
            dt = datetime.strptime(sanitized_value, '%Y-%m-%dT%H:%M:%SZ')
            return int(dt.timestamp())  # Convert RFC3339 to Unix Epoch time
        except ValueError:
            return sanitized_value if sanitized_value else None

    # Handle 'N' (Number) type
    if 'N' in value:
        sanitized_value = value['N'].strip()
        if sanitized_value.replace('.', '', 1).isdigit():  # Check if it's a valid number
            sanitized_value = sanitized_value.lstrip('0') or '0'
            if '.' in sanitized_value:
                return float(sanitized_value)
            return int(sanitized_value)
        return None  # Invalid number, return None

    # Handle 'BOOL' (Boolean) type
    if 'BOOL' in value:
        bool_value = value['BOOL'].strip().lower()
        if bool_value in ['1', 't', 'true']:
            return True
        elif bool_value in ['0', 'f', 'false']:
            return False
        return None  # Invalid boolean value, return None

    # Handle 'NULL' type
    if 'NULL' in value:
        null_value = value['NULL'].strip().lower()
        if null_value in ['1', 't', 'true']:
            return None  # Represent null
        elif null_value in ['0', 'f', 'false']:
            return False  # Omit null-equivalent values
        return None  # Invalid null value, return None

    # Handle 'L' (List) type
    if 'L' in value:
        transformed_list = []
        for item in value['L']:
            transformed_item = transform_value('', item)
            if transformed_item is not None and transformed_item != '':
                transformed_list.append(transformed_item)
        return transformed_list if transformed_list else None

    # If none of the expected types match, return None
    return None

def transform_input(data):
    transformed_data = {}

    for key, value in data.items():
        sanitized_key = key.strip()
        if not sanitized_key:  # Skip if key is empty
            continue

        # Process Maps (M) and Lists (L) recursively
        if 'M' in value:
            transformed_map = transform_input(value['M'])
            if transformed_map:  # Omit empty maps
                transformed_data[sanitized_key] = transformed_map
        elif 'L' in value and isinstance(value['L'], list):
            transformed_list = transform_value(sanitized_key, value)
            if transformed_list:  # Omit empty lists
                transformed_data[sanitized_key] = transformed_list
        else:
            transformed_value = transform_value(sanitized_key, value)
            if transformed_value is not None:  # Omit invalid or empty values
                transformed_data[sanitized_key] = transformed_value

    return transformed_data

# Read input JSON
input_json = """
{
  "number_1": {
    "N": "1.50"
  },
  "string_1": {
    "S": "784498 "
  },
  "string_2": {
    "S": "2014-07-16T20:55:46Z"
  },
  "map_1": {
    "M": {
      "bool_1": {
        "BOOL": "truthy"
      },
      "null_1": {
        "NULL": "true"
      },
      "list_1": {
        "L": [
          {
            "S": ""
          },
          {
            "N": "011"
          },
          {
            "N": "5215s"
          },
          {
            "BOOL": "f"
          },
          {
            "NULL": "0"
          }
        ]
      }
    }
  },
  "list_2": {
    "L": "noop"
  },
  "list_3": {
    "L": [
      "noop"
    ]
  },
  "": {
    "S": "noop"
  }
}
"""

data = json.loads(input_json)
transformed_data = [transform_input(data)]

# Output the result
print(json.dumps(transformed_data, indent=2))
