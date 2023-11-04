import tornado.web
import tornado.ioloop

# Inventory Management Section
class Item:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def check_low_stock(self):
        low_stock_items = [item.name for item in self.items if item.quantity < 5]
        return low_stock_items

    def calculate_total_value(self):
        total_value = sum(item.quantity * item.price for item in self.items)
        return total_value

    def delete_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                break

    def search_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return None

# Tornado Request Handlers
inventory = Inventory()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the Inventory Management System!")

class AddItemHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name")
        quantity = int(self.get_argument("quantity"))
        price = float(self.get_argument("price"))

        inventory.add_item(Item(name, quantity, price))
        self.write(f"Item '{name}' has been added.")

class DeleteItemHandler(tornado.web.RequestHandler):
    def get(self):
        item_name = self.get_argument("name")
        inventory.delete_item(item_name)
        self.write(f"Item '{item_name}' has been deleted.")

class SearchItemHandler(tornado.web.RequestHandler):
    def get(self):
        item_name = self.get_argument("name")
        item = inventory.search_item(item_name)
        if item:
            self.write(f"Item found: {item.name}, {item.quantity}, {item.price}")
        else:
            self.write("Item not found.")

class CheckLowStockHandler(tornado.web.RequestHandler):
    def get(self):
        low_stock_items = inventory.check_low_stock()
        if low_stock_items:
            self.write("Items running low: " + ', '.join(low_stock_items))
        else:
            self.write("No items running low.")

class CalculateTotalValueHandler(tornado.web.RequestHandler):
    def get(self):
        total_value = inventory.calculate_total_value()
        self.write("Total value of inventory: $" + str(total_value))

class StaticHandler(tornado.web.RequestHandler):
    def get(self):
        with open('static/index.html', 'r') as f:
            self.write(f.read())

# Tornado Application Setup
app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/add_item", AddItemHandler),
    (r"/delete_item", DeleteItemHandler),
    (r"/search_item", SearchItemHandler),
    (r"/check_low_stock", CheckLowStockHandler),
    (r"/calculate_total_value", CalculateTotalValueHandler),
    (r"/static/index.html", StaticHandler),  # Serving index.html
])

if __name__ == "__main__":
    print("Starting the server...")
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
