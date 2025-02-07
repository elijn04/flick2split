import streamlit as st

class Guest:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.subtotal = 0
        self.tax = 0
        self.tip = 0
        self.total = 0

    def add_item(self, item_name, price):
        self.items.append({"name": item_name, "price": price})
        self.subtotal += price

    def calculate_tax_and_tip(self, overall_subtotal, overall_tax, tip_percentage):
        if overall_subtotal > 0:
            proportion = self.subtotal / overall_subtotal
            self.tax = overall_tax * proportion
            self.tip = self.subtotal * (tip_percentage / 100)
            self.total = self.subtotal + self.tax + self.tip

    def display_summary(self):
        for item in self.items:
            st.write(f"- {item['name']} (${item['price']:.2f})")
        st.write(f"**Tax:** ${self.tax:.2f}")
        st.write(f"**Tip:** ${self.tip:.2f}")
    
    def display_super_summary(self):
        st.write(f"**{self.name}'s** Total Owed: **${self.total:.2f}**")

    def get_items_for_return(self):
        """Return items in the format needed for the available items list"""
        return [{"Name": item["name"], "Quantity": 1, "Price": item["price"]} for item in self.items]