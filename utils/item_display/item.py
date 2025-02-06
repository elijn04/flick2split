class Item:
    """
    Represents an item from the receipt with its properties and related calculations.
    """
    def __init__(self, name: str, quantity: int, price: float, split_count: int = 1):
        self.name = name
        self.quantity = quantity
        self.total_price = price
        self.split_count = split_count
        self.price_per_unit = self._calculate_price_per_unit()
        
    def _calculate_price_per_unit(self) -> float:
        """Calculate the price per unit of the item."""
        return self.total_price / self.quantity if self.quantity > 0 else 0.0
    
    def is_valid(self) -> bool:
        """Check if the item has valid price and quantity."""
        return self.total_price > 0 and self.quantity > 0
    
    def decrease_quantity(self, amount: int = 1) -> None:
        """
        Decrease the quantity of the item and update its price accordingly.
        
        Args:
            amount (int): Amount to decrease by (default: 1)
        """
        if amount <= self.quantity:
            self.quantity -= amount
            self.total_price -= (self.price_per_unit * amount)
    
    def to_dict(self) -> dict:
        """Convert item to dictionary format."""
        return {
            "Name": self.name,
            "Quantity": self.quantity,
            "Price": self.total_price
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        """
        Create an Item instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing item data with keys 'Name', 'Quantity', and 'Price'
        
        Returns:
            Item: New Item instance
        """
        return cls(
            name=data["Name"],
            quantity=data["Quantity"],
            price=data["Price"]
        )
    
    def split_item(self, split_count: int) -> list['Item']:
        """
        Split an item into multiple items with divided prices.
        
        Args:
            split_count (int): Number of ways to split the item
            
        Returns:
            list[Item]: List of split items
        """
        if split_count <= 1:
            return [self]
            
        split_price = self.total_price / split_count
        split_items = []
        
        for _ in range(split_count):
            split_items.append(
                Item(
                    name=f"1/{split_count} {self.name}",
                    quantity=self.quantity,
                    price=split_price,
                    split_count=split_count
                )
            )
        
        return split_items 