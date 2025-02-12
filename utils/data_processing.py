def parse_receipt_data(raw_data):
    parsed_data = {}
    for line in raw_data.split("\n"):
        try:
            if "Store Name" in line:
                parsed_data['Store Name'] = line.split(': ')[1].strip('" ,')
            elif "Date" in line:
                parsed_data['Date'] = line.split(': ')[1].strip('" ,')
            elif "Time" in line:
                parsed_data['Time'] = line.split(': ')[1].strip('" ,')
            elif "Subtotal" in line:
                value = line.split(': ')[1].strip('" ,')
                if value.lower() != 'null' and value.strip() != '':
                    # Remove any currency symbols and commas before converting
                    value = value.replace('$', '').replace(',', '').strip()
                    parsed_data['Subtotal'] = float(value)
                else:
                    parsed_data['Subtotal'] = None
            elif "Tax" in line:
                value = line.split(': ')[1].strip('" ,')
                if value.lower() != 'null' and value.strip() != '':
                    value = value.replace('$', '').replace(',', '').strip()
                    parsed_data['Tax'] = float(value)
                else:
                    parsed_data['Tax'] = None
            elif "Total" in line:
                value = line.split(': ')[1].strip('" ,')
                if value.lower() != 'null' and value.strip() != '':
                    value = value.replace('$', '').replace(',', '').strip()
                    parsed_data['Total'] = float(value)
                else:
                    parsed_data['Total'] = None
        except (ValueError, IndexError) as e:
            print(f"Error processing line: {line}")
            print(f"Error: {e}")
    return parsed_data

def extract_items(raw_data):
    items_start = raw_data.find('"Items": [') + len('"Items": [')
    items_end = raw_data.find(']', items_start)
    items_data = raw_data[items_start:items_end].strip()

    item_list = []
    for item in items_data.split('},'):
        if item.strip():  # Check if the item block is not empty
            item = item.strip("{}, \n")
            item_dict = {}
            for detail in item.split(','):
                try:
                    key, value = detail.split(':')
                    key = key.strip('" ')
                    value = value.strip('" ')
                    if key == 'Price':
                        if value.lower() != 'null' and value.strip() != '':
                            # Remove any currency symbols and commas before converting
                            value = value.replace('$', '').replace(',', '').strip()
                            value = float(value)
                        else:
                            value = None
                    elif key == 'Quantity':
                        if value.lower() != 'null' and value.strip() != '':
                            value = int(value)
                        else:
                            value = 1  # if there is an item value must be 1
                    item_dict[key] = value
                except ValueError as e:
                    print(f"Error processing detail: {detail}")
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error processing detail: {detail}")
                    print(f"Error: {e}")
            item_list.append(item_dict)

    return item_list

def manually_parse_to_dict(raw_data):
    # Parse the raw receipt data
    parsed_data = parse_receipt_data(raw_data)

    # Extract items from the raw data
    items = extract_items(raw_data)

    # Add the items list to the parsed_data dictionary
    parsed_data['items'] = items

    return parsed_data