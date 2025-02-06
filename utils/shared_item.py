class SharedItem:
    def __init__(self, item, num_shares):
        """
        Initialize a shared item with the original item details and number of shares.
        
        Args:
            item (dict): Original item with 'Name' and 'Price' keys
            num_shares (int): Number of ways to split the item
        """
        self.original_item = item
        self.num_shares = num_shares
        self.split_price = round(item['Price'] / num_shares, 2)
        self.total_price = item['Price']
        self.split_name = f"1/{num_shares} {item['Name']}"
        self.quantity = num_shares
    
    def to_dict(self):
        """Convert the shared item to a dictionary format."""
        return {
            'Name': self.split_name,
            'Quantity': self.quantity,
            'Price': self.total_price
        }

def update_shared_receipt_data(receipt_data, shared_items, shares_count):
    """
    Update receipt data with shared items split into portions.
    
    Args:
        receipt_data (dict): Original receipt data
        shared_items (list): List of items to be shared
        shares_count (int): Number of ways to split each shared item
    
    Returns:
        dict: Updated receipt data with shared items split
    """
    # Create a new dictionary for the updated receipt
    shared_receipt = receipt_data.copy()
    new_items = []
    
    # Process each item from the original receipt
    for item in receipt_data['items']:
        # Check if this item is in shared_items
        if item in shared_items:
            # Create a SharedItem instance and add the split version
            shared_item = SharedItem(item, shares_count)
            new_items.append(shared_item.to_dict())
        else:
            # Keep non-shared items as they are
            new_items.append(item)
    
    # Update the items list in the receipt
    shared_receipt['items'] = new_items
    return shared_receipt 