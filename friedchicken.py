# Program Developer Name: Michael Boyer
#
# Date Program Developed: 04/08/2025
#
# Organization: CIS 202 - 302
#
# Description: Display a menu with GUI elements for the Calhoun Fried Chicken restaurant based on items from pictures of the board. Save the order to a data structure and print orders (at least 5).
#
# Document your givens below this line
#
# Document your inputs below this line
#
# Document your outputs below this line
#
# Document your processes below this line
#
# Start your program code after this line

import tkinter as tk

class CalhounFriedChicken:
    # Constants for pricing and items
    TAX_RATE = 0.09
    COMBO_DISCOUNT = 0.05
    MEAL_DISCOUNTS = {"regular": 0.10, "large": 0.15}

    # Constants for GUI
    FONT_SIZES = {
        "xl": ("Comic Sans MS", 28),
        "lg": ("Comic Sans MS", 14),
        "md": ("Comic Sans MS", 12),
        "sm": ("Comic Sans MS", 10)
    }

    def __init__(self):
        # Main window setup
        self.main_window = tk.Tk()
        self.main_window.title("Calhoun Fried Chicken")
        self.main_window.geometry("720x880")

        self.current_frame = None
        self.container = tk.Frame(self.main_window)
        self.container.pack(expand=True, fill='both')

        # Initialize cart and orders lists
        self.cart = []
        self.orders = []

        # Initialize menu dictionaries
        self.entrees = {
            "name": "Entrées",
            "part_of_meal": True,
            "meal_step": 1,
            "items": {
                "tender_bucket": {
                    "name": "Tenders Bucket",
                    "description": "A bucket of delicious chicken tenders, fried or grilled.",
                    "piece": [2, 4, 6, 10, 12],
                    "price": [4.0, 8.0, 12.0, 20.0, 24.0],
                    "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                    "dark_or_light": True
                },
                "nugget_bucket": {
                    "name": "Nugget Bucket",
                    "description": "A bucket of scrumptious chicken nuggets, fried or grilled.",
                    "piece": [5, 10, 15, 25, 30],
                    "price": [2.0, 4.0, 6.0, 10.0, 12.0],
                    # Assuming same flavors apply
                    "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                    "dark_or_light": True  # Assuming nuggets are typically white meat
                },
                "chicken_sandwich": {
                    "name": "Chicken Sandwich",
                    "description": "Three of our juicy tenders, fried or grilled, on fluffy toasted bread with mayo, pickles, lettuce and tomato.",
                    "piece": [1],  # Represents one sandwich
                    "price": [5.0],
                    "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                    "dark_or_light": False  # Sandwich uses tenders, choice might be implicit or not offered
                },
                "chicken_salad": {
                    "name": "Chicken Salad",
                    "description": "Our grilled tenders make it into a salad with creamy dressing and fresh veggies.",
                    "piece": [1],  # Represents one salad
                    "price": [5.0],
                    # Flavors specific to salad tenders
                    "flavor": ["Cajun Grilled", "Spicy Grilled", "Classic Grilled"],
                    "dark_or_light": False  # Salad, meat type choice not typical
                }
            }
        }
        self.sides = {
            "name": "Sides",
            "part_of_meal": True,
            "meal_step": 2,
            "items": {
                "fries": {
                    "name": "Fries",
                    "description": "Crispy crinkle-cut fries with a sprinkle of sea salt.",
                    "piece": ["individual", "family"],
                    "price": [2.0, 4.0],
                    "premium": False
                },
                "mashed_potatoes": {
                    "name": "Mashed Potatoes",
                    "description": "Our fluffy mashed potatoes made every morning.",
                    "piece": ["individual", "family"],
                    "price": [2.0, 4.0],
                    "premium": False
                },
                "collard_greens": {
                    "name": "Collard Greens",
                    "description": "Slow-cooked collard greens seasoned with smoked meat and spices for a classic Southern flavor.",
                    "piece": ["individual", "family"],
                    "price": [2.0, 4.0],
                    "premium": False
                },
                "cornbread": {
                    "name": "Cornbread (2pc)",
                    "description": "Sweet and buttery cornbread with a hint of diced jalapeño.",
                    # Assuming individual = 2pc, family = more
                    "piece": ["individual", "family"],
                    "price": [2.0, 4.0],  # Prices might vary
                    "premium": False
                },
                "biscuits": {
                    "name": "Biscuits (2pc)",
                    "description": "Fluffy and buttery biscuits—a match made in heaven with our chicken.",
                    # Assuming individual = 2pc, family = more
                    "piece": ["individual", "family"],
                    "price": [2.0, 4.0],
                    "premium": False
                },
                "mac_and_cheese": {
                    "name": "Mac and Cheese",
                    "description": "A creamy and decadent mac and cheese baked to perfection.",
                    "piece": ["individual", "family"],
                    "price": [3.0, 5.0],
                    "premium": True  # Often considered premium
                },
                "green_beans": {
                    "name": "Smoked Green Beans with Bacon",
                    "description": "Tender green beans smoked with bacon and spices.",
                    "piece": ["individual", "family"],
                    "price": [3.0, 5.0],
                    "premium": True  # Often considered premium
                }
            }
        }
        self.drinks = {
            "name": "Drinks",
            "part_of_meal": True,
            "meal_step": 3,
            "items": {
                "fountain_drink": {
                    "name": "Fountain Drink",
                    "description": "Choose from a variety of refreshing beverages. Options available: lemonade, Coke, Sprite, and Dr. Pepper.",
                    "piece": ["medium", "large"],
                    "price": [2.0, 3.0]
                },
                "milk": {
                    "name": "Milk",
                    "description": "A carton of milk.",
                    "piece": ["packaged"],
                    "price": [2.0]
                },
                "chocolate_milk": {
                    "name": "Chocolate Milk",
                    "description": "A carton of chocolate milk.",
                    "piece": ["packaged"],
                    "price": [2.0]
                },
                "iced_tea": {
                    "name": "Iced Tea (by the gallon)",
                    "description": "A gallon of refreshing iced tea, sweet or unsweetened.",
                    "piece": ["gallon_sweet", "gallon_unsweet"],
                    "price": [5.0, 5.0]
                },
                "fruit_juice": {
                    "name": "Fruit Juice",
                    "description": "A carton of fruit juice, apple or orange.",
                    "piece": ["packaged_apple", "packaged_orange"],
                    "price": [3.0]
                },
                "bottled_water": {
                    "name": "Bottled Water",
                    "description": "The original thirst quencher.",
                    "piece": ["packaged"],
                    "price": [0.0]  # Or a price like 1.50
                }
            }
        }
        self.desserts = {
            "name": "Desserts",
            "part_of_meal": True,
            "meal_step": 4,
            "items": {
                "cookie": {
                    "name": "Cookie",
                    "description": "A freshly baked cookie, available in chocolate chip, oatmeal raisin, or sugar.",
                    "piece": ["chocolate chip", "oatmeal raisin", "sugar"],
                    "price": [2.0, 2.0, 2.0]
                },
                "brownie": {
                    "name": "Brownie",
                    "description": "A rich and fudgy brownie.",
                    "piece": ["individual"],
                    "price": [2.0]
                },
                "apple_pie": {
                    "name": "Apple Pie",
                    "description": "A slice of classic apple pie with a flaky crust.",
                    "piece": ["individual"],
                    "price": [4.0]
                },
                "cheesecake": {
                    "name": "Cheesecake",
                    "description": "A slice of creamy cheesecake with a graham cracker crust.",
                    "piece": ["individual"],
                    "price": [4.0]
                },
                "cobbler": {
                    "name": "Cobbler",
                    "description": "A square of warm cobbler with a buttery crust, available with peach or blackberry.",
                    "piece": ["peach", "blackberry"],
                    "price": [4.0, 4.0]
                }
            }
        }
        self.combos = {
            "name": "Combos",
            "part_of_meal": False,
            "items": {
                "mix_tender_combo": {
                    "name": "Mix & Match Combo",
                    "description": "Save 5% on a bucket of tenders with light and dark meat mixed and matched.",
                    # Informational text
                    "mix_match_rule": "You must pick in sets of 2 tenders between light or dark meat.",
                    "mix_increment": 2,  # Slider resolution
                    "piece": [10, 12],  # Total pieces options
                    # Price for total pieces BEFORE discount
                    "price": [20.0, 24.0],
                    "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                    "combo_discount": self.COMBO_DISCOUNT  # Reference constant
                },
                "tender_combo": {
                    "name": "Tenders Combo",
                    "description": "Save 5% on a 4/6pc bucket of tenders with light or dark meat.",
                    "piece": [4, 6],
                    "price": [8.0, 12.0],  # Price BEFORE discount
                    "dark_or_light": True,
                    # Added flavor
                    "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                    "combo_discount": self.COMBO_DISCOUNT  # Reference constant
                }
            }
        }
        self.meals = {
            "name": "Meals",
            "part_of_meal": False,
            "items": {
                "regular_meal": {
                    "name": "Regular Meal",
                    "description": "1 entree, 1 side, 1 drink, and 1 dessert - Save 10%!",
                    "piece": [1],  # Represents one meal
                    "price": [0.0],  # Price calculated from components
                    "requirements": {
                        "entrees": 1,
                        "sides": 1,
                        "drinks": 1,
                        "desserts": 1
                    },
                    # Reference constant
                    "discount": self.MEAL_DISCOUNTS["regular"]
                },
                "large_meal": {
                    "name": "Large Meal",
                    "description": "1 entree, 2 sides, 1 drink, and 1 dessert - Save 15%!",
                    "piece": [1],  # Represents one meal
                    "price": [0.0],  # Price calculated from components
                    "requirements": {
                        "entrees": 1,
                        "sides": 2,  # Requires two sides
                        "drinks": 1,
                        "desserts": 1
                    },
                    # Reference constant
                    "discount": self.MEAL_DISCOUNTS["large"]
                }
            }
        }

        self.show_start()

    def switch_frame(self, frame):
        # If the frame is already displayed, do nothing
        if self.current_frame == frame:
            return

        # Destroy the current frame if it exists
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack()

    def show_start(self):
        frame = tk.Frame(self.container)

        # Create the welcome label
        welcome = tk.Label(frame, text='Welcome', font=self.FONT_SIZES["xl"])
        welcome.pack(pady=(20, 0))
        to_cfc = tk.Label(frame, text='to Calhoun Fried Chicken!', font=self.FONT_SIZES["lg"])
        to_cfc.pack(pady=(0, 20))

        # Create the instructions label
        instructions = tk.Label(frame, text='Start your order by clicking the button below.', font=self.FONT_SIZES["md"])
        instructions.pack(pady=10)

        # Create the start button
        start_button = tk.Button(frame, text="Start Order", command=self.show_categories, font=self.FONT_SIZES["md"], width=30, height=5)
        start_button.pack(side=tk.BOTTOM, pady=10)

        self.switch_frame(frame)

    def show_categories(self):
        frame = tk.Frame(self.container)

        title = tk.Label(frame, text="Select a category", font=self.FONT_SIZES["lg"])
        title.pack(pady=20)

        button_frame = tk.Frame(frame)
        button_frame.pack()
        button_frame.pack()

        # All categories
        categories = [self.entrees, self.sides, self.drinks, self.desserts, self.combos, self.meals]

        # Create buttons for each category in a grid layout
        for i, category in enumerate(categories):
            category_name = category["name"]
            row = i // 2
            col = i % 2
            category_button = tk.Button(
                button_frame,
                text=category_name,
                command=lambda k=category: self.show_category(k),
                font=self.FONT_SIZES["md"],
                width=20,
                height=5)
            category_button.grid(row=row, column=col, padx=10, pady=10)

        cart_frame = tk.Frame(frame)
        cart_frame.pack(pady=15)

        cart_button = tk.Button(cart_frame, text="View Cart", command=self.view_cart, font=self.FONT_SIZES["md"], width=15)
        cart_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(cart_frame, text="Back", command=self.show_start, font=self.FONT_SIZES["md"])
        back_button.pack(padx=5,pady=10)

        self.switch_frame(frame)

    def show_category(self, category):
            frame = tk.Frame(self.container)

            # If category exists, display category items
            if category:
                # Create a title for the category
                title = tk.Label(frame, text=category["name"], font=self.FONT_SIZES["xl"])
                title.pack(pady=20)

                # Get all the items in the category.
                items = category["items"]

                for key, value in items.items():

                    # Begin items container in the frame
                    item_container = tk.Frame(frame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
                    item_container.pack(pady=5, fill=tk.X)

                    # If the item has a flag of "premium": True, we need to append "(Premium)" to the item name.
                    if "premium" in value and value["premium"]:
                        item_name = value["name"] + " (Premium)"
                    else:
                        item_name = value["name"]

                    # Add item labels to container
                    tk.Label(item_container, text=item_name, font=self.FONT_SIZES["md"], anchor=tk.W).pack(anchor=tk.W)
                    tk.Label(item_container, text=value["description"], font=self.FONT_SIZES["sm"], wraplength=600, anchor=tk.W).pack(anchor=tk.W)

                    if key == "regular_meal" or key == "large_meal":
                        tk.Button(item_container, text="Customize", command=lambda category=category, key=key: self.build_meal(category, key), font=self.FONT_SIZES["md"]).pack(anchor=tk.E)
                    elif key == "mix_tender_combo":
                        tk.Button(item_container, text="Select", command=lambda category=category, key=key: self.show_mix_match(category, key), font=self.FONT_SIZES["md"]).pack(anchor=tk.E)
                    else:
                        tk.Button(item_container, text="Select", command=lambda category=category, key=key: self.show_item(category, key), font=self.FONT_SIZES["md"]).pack(anchor=tk.E)

            # If category does not exist, display under construction message
            else:
                tk.Label(frame, text="Under construction", font=self.FONT_SIZES["lg"]).pack(pady=20)
                tk.Label(frame, text="This category is coming soon!", font=self.FONT_SIZES["md"]).pack(pady=10)

            # Back button for both cases
            tk.Button(frame, text="Back", command=self.show_categories, font=self.FONT_SIZES["md"]).pack(pady=10)
            self.switch_frame(frame)

    def show_item(self, category, key):
        frame = tk.Frame(self.container)

        # Labels for name and description of item
        tk.Label(frame, text=category["items"][key]["name"], font=self.FONT_SIZES["xl"]).pack(pady=10)
        tk.Label(frame, text=category["items"][key]["description"], font=self.FONT_SIZES["md"], wraplength=500).pack(pady=5)

        options = self.item_options_helper(frame, category["items"][key])
        options.pack(pady=10, fill=tk.X)

        tk.Button(frame, text="Add to Cart", command=lambda: self.add_to_cart(category, key, options), font=self.FONT_SIZES["md"]).pack(pady=20)

        # Button to go back to the category screen
        tk.Button(
            frame,
            text="Back to Items",
            command=lambda k=category: self.show_category(k),
            font=self.FONT_SIZES["md"]).pack(pady=10)
        self.switch_frame(frame)

    def show_mix_match(self, category, key):
        # TODO: Add mix and match flow from old version of program
        return

    def build_meal(self, category, key):
        # TODO: Refine meal builder flow from old version of program
        return

    def view_cart(self):
        # TODO: Add cart view from old version of program
        return

    def add_to_cart(self, category, key, options):
        # TODO: Add function to add something to cart from old version of program
        return

    ## - - - - Helper functions - - - - ##

    def item_options_helper(self, frame, item):
        options = tk.Frame(frame)
        options.pack(pady=10, fill=tk.X)

        # Create variables to hold selected options
        options.selected_size = tk.StringVar()
        options.selected_flavor = tk.StringVar()
        options.selected_meat_type = tk.StringVar()

        # Use size, flavor and meat selection helper functions
        self.size_selection_helper(options, item)
        self.flavor_selection_helper(options, item)
        self.meat_selection_helper(options, item)
        return options

    def size_selection_helper(self, options, item):
        # If pc/size/qty is in the item data, and a value exists, we create a frame.
        if "piece" in item and len(item["piece"]) > 0:
            size_frame = tk.LabelFrame(options,
                                       text="Select Quantity",
                                       padx=10,
                                       pady=10)
            size_frame.pack(fill=tk.X, padx=10, pady=5)

            # Loop through the pieces and prices and create a radio button
            for i, (piece, price) in enumerate(zip(item["piece"], item["price"])):
                if isinstance(piece, int):
                    text =  f"{piece} pc - ${price:.2f}"
                else:
                    text = f"{piece.capitalize()} - ${price:.2f}"
                tk.Radiobutton(size_frame,
                               text=text,
                               variable=options.selected_size,
                               value=str(i),
                               font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options.selected_size.set("0")

    def flavor_selection_helper(self, options, item):
        # If flavor is in the item data, we create a frame for it
        if "flavor" in item and len(item["flavor"]) > 0:
            flavor_frame = tk.LabelFrame(options,
                                         text="Select Flavor",
                                         padx=10,
                                         pady=10)
            flavor_frame.pack(fill=tk.X, padx=10, pady=5)

            # For each flavor, make that radio button.
            for i, flavor in enumerate(item["flavor"]):
                tk.Radiobutton(flavor_frame,
                               text=flavor,
                               variable=options.selected_flavor,
                               value=str(i),
                               font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options.selected_flavor.set("0")

    def meat_selection_helper(self, options, item):
        # If meat is in the item data, we create a frame for it
        if "dark_or_light" in item and item["dark_or_light"]:
            meat_frame = tk.LabelFrame(options,
                                       text="Select Meat",
                                       padx=10,
                                       pady=10)
            meat_frame.pack(fill=tk.X, padx=10, pady=5)

            # For each meat, make that radio button.
            tk.Radiobutton(meat_frame,
                           text="Light Meat (white meat, breast and wing)",
                           variable=options.selected_meat_type,
                           value="light",
                           font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            tk.Radiobutton(meat_frame,
                           text="Dark Meat (dark meat, thigh and leg)",
                           variable=options.selected_meat_type,
                           value="dark",
                           font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options.selected_meat_type.set("light")

    def run(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = CalhounFriedChicken()
    app.run()
