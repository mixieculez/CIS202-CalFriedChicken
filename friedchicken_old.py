# Program Developer Name:  Michael Boyer
#
# Date Program Developed:  04/01/2025
#
# Organization: CIS 202 - 302
#
# Description: Display a menu with GUI elements for the Calhoun Fried Chicken restaurant based on
# items from pictures of the board. Save the order to a data structure and print orders (at least 5).

# Document your givens below this line
# - Tax Rate: 9% (0.09)
# - Font Sizes: Predefined dictionary (xl, lg, md, sm) with Comic Sans MS font.
# - Combo Discount: 5% (0.05)
# - Meal Discounts: Regular Meal/Meal A 10% (0.10), Large Meal/Meal B 15% (0.15).
# - Menu Data: A nested dictionary containing categories, items, names, descriptions,
#   available sizes/pieces, prices per size/pieces, available flavors, meat type options (dark/light),
#   premium status for sides, combo rules (mix & match increment), and meal requirements.
# - Specific item names, descriptions, prices, sizes, flavors as defined in the `self.menu` dictionary.
#
# Document your inputs below this line
# - User clicks on buttons (Start Order, Category buttons, Item 'Select'/'Customize' buttons,
#   'Add to Cart', 'View Cart', 'Back', 'Checkout', 'Back to Start').
# - User selections via radio buttons for:
#   - Item Size/Quantity
#   - Item Flavor
#   - Item Meat Type (Light/Dark)
#   - Mix & Match Combo: Total pieces
#   - Mix & Match Combo: Flavor
# - User input via slider for:
#   - Mix & Match Combo: Light vs Dark meat ratio
# - User selections during meal building process (choosing one item per required category)
# - User responses to message boxes (e.g., confirming cancellation of a meal)
#
# Document your outputs below this line
# - Graphical User Interface display:
#   - Welcome Screen.
#   - Category Selection Screen.
#   - Item Selection Screen (listing items within a category).
#   - Item Customization Screen (options for size, flavor, etc.).
#   - Mix & Match Combo Customization Screen.
#   - Cart View Screen:
#     - List of items added.
#     - Details for each item (size, flavor, meat type, components for meals/combos).
#     - Individual item prices.
#     - Applied discounts (combo/meal).
#     - Subtotal.
#     - Sales Tax amount.
#     - Total order cost.
#   - Checkout Screen:
#     - Final order summary (similar to cart view).
#     - Thank you message.
# - Message Boxes:
#   - Information messages (e.g., "Item added to cart", "Select [category] for your meal").
#   - Error messages (e.g., "Invalid selection", "Missing required meal items").
#   - Confirmation messages (e.g., asking to cancel meal building).
#
# Document your processes below this line
# Initialization
#     - Create the main window.
#     - Set up important values (tax, discounts, text styles).
#     - Set up the menu items in an organized way.
#     - Create an empty shopping cart.
#     - Get ready to build meals if needed.
#     - Show the welcome screen.
# Navigation
#     - Switch between different screens when buttons are clicked.
#     - Make sure "Back" buttons work correctly.
# Menu Categories
#     - Show food categories from our menu data.
#     - Show items in each category with names and descriptions.
#     - Mark special sides that cost extra.
# Selecting Items
#     - Show options for each item (size, flavor, type of meat).
#     - Save what the customer picks.
#     - Pick default options if customer doesn't choose.
# Handling Combos
#     - Special screen for mix-and-match combos.
#     - Let customers pick light/dark meat ratio.
#     - Figure out combo prices with discounts.
# Building Meals
#     - Start putting together a meal when picked.
#     - Guide customers through picking each part.
#     - Make sure they pick everything needed.
#     - Handle large meals needing extra sides.
#     - Save all choices and calculate price with discount.
#     - Reset everything when done or canceled.
# Managing Cart
#     - Add items to cart with all choices and prices.
#     - Show what's in the cart.
#     - Add up prices, discounts, and tax.
#     - Let customers scroll through large orders.
# Working with Prices
#     - Get basic prices from menu.
#     - Apply combo discounts (5% off).
#     - Add up meal prices and apply meal discounts (10% or 15% off).
#     - Calculate tax.
#     - Show final price.
# Checking Out
#     - Show final order details.
#     - Thank the customer.
#     - Empty the cart.
# Handling Mistakes
#     - Provide error dialogs with user input mismatch.
#     - Catch exceptions for better debugging.
#     - Handle unexpected errors gracefully.
# Helper Tools
#     - Use special functions for text formatting and item selections.
# -----------------------------------------------------
# Start your program code after this line

import tkinter as tk
from tkinter import messagebox


class CalhounFriedChicken:
    # Constants for tax rate, preset font sizes, combo discount, and meal discount keys
    TAX_RATE = 0.09
    FONT_SIZES = {
        "xl": ("Comic Sans MS", 28),
        "lg": ("Comic Sans MS", 14),
        "md": ("Comic Sans MS", 12),
        "sm": ("Comic Sans MS", 10)
    }
    COMBO_DISCOUNT = 0.05  # 5% discount for combos
    MEAL_DISCOUNT_KEYS = {"regular": "regular_meal", "large": "large_meal"}

    def __init__(self):
        # Main window setup
        self.main_window = tk.Tk()
        self.main_window.title("Calhoun Fried Chicken")
        self.main_window.geometry('720x880')
        self.current_frame = None
        self.container = tk.Frame(self.main_window)
        self.container.pack(expand=True, fill='both')
        self.cart = []
        self.MEAL_DISCOUNTS = {"regular": 0.10, "large": 0.15}
        self.meal_builder = None  # Initialize meal_builder attribute

        # Initialize menu data in a dictionary
        # Using a more data-driven approach to define the menu because it lets us change the menu
        # however we want without having to change the core logic (for the most part, since we have to
        # do some extra stuff around the meals and combos).
        self.menu = {
            "category": {
                "entrees": {
                    "name": "Entrées",  # Display name for the category
                    "part_of_meal": True,  # Whether this is part of a meal
                    "meal_step": 1,  # Step in the meal-building process
                    "item": {
                        "tender_bucket": {
                            "name": "Tenders Bucket",
                            "description":
                            "A bucket of delicious chicken tenders, fried or grilled.",
                            "piece": [2, 4, 6, 10, 12],
                            "price": [4.0, 8.0, 12.0, 20.0, 24.0],
                            "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                            "dark_or_light": True
                        },
                        "nugget_bucket": {
                            "name": "Nugget Bucket",
                            "description":
                            "A bucket of scrumptious chicken nuggets, fried or grilled.",
                            "piece": [5, 10, 15, 25, 30],
                            "price": [2.0, 4.0, 6.0, 10.0, 12.0],
                            "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                            "dark_or_light": True
                        },
                        "chicken_sandwich": {
                            "name": "Chicken Sandwich",
                            "description":
                            "Three of our juicy tenders, fried or grilled, on fluffy toasted bread with mayo, pickles, lettuce and tomato.",
                            "piece": [1],
                            "price": [5.0],
                            "flavor": ["Cajun", "Spicy", "Classic", "Grilled"],
                            "dark_or_light": False
                        },
                        "chicken_salad": {
                            "name":
                            "Chicken Salad",
                            "description":
                            "Our grilled tenders make it into a salad with creamy dressing and fresh veggies.",
                            "piece": [1],
                            "price": [5.0],
                            "flavor": [
                                "Cajun Grilled", "Spicy Grilled",
                                "Classic Grilled"
                            ],
                            "dark_or_light":
                            False
                        }
                    }
                },
                "sides": {
                    "name": "Sides",
                    "part_of_meal": True,
                    "meal_step": 2,
                    "item": {
                        "fries": {
                            "name": "Fries",
                            "description":
                            "Crispy crinkle-cut fries with a sprinkle of sea salt.",
                            "piece": ["individual", "family"],
                            "price": [2.0, 4.0],
                            "premium": False
                        },
                        "mashed_potatoes": {
                            "name": "Mashed Potatoes",
                            "description":
                            "Our fluffy mashed potatoes made every morning.",
                            "piece": ["individual", "family"],
                            "price": [2.0, 4.0],
                            "premium": False
                        },
                        "collard_greens": {
                            "name": "Collard Greens",
                            "description":
                            "Slow-cooked collard greens seasoned with smoked meat and spices for a classic Southern flavor.",
                            "piece": ["individual", "family"],
                            "price": [2.0, 4.0],
                            "premium": False
                        },
                        "cornbread": {
                            "name": "Cornbread (2pc)",
                            "description":
                            "Sweet and buttery cornbread with a hint of diced jalapeño.",
                            "piece": ["individual", "family"],
                            "price": [2.0, 4.0],
                            "premium": False
                        },
                        "biscuits": {
                            "name": "Biscuits (2pc)",
                            "description":
                            "Fluffy and buttery biscuits—a match made in heaven with our chicken.",
                            "piece": ["individual", "family"],
                            "price": [2.0, 4.0],
                            "premium": False
                        },
                        "mac_and_cheese": {
                            "name": "Mac and Cheese",
                            "description":
                            "A creamy and decadent mac and cheese baked to perfection.",
                            "piece": ["individual", "family"],
                            "price": [3.0, 5.0],
                            "premium": True
                        },
                        "green_beans": {
                            "name": "Smoked Green Beans with Bacon",
                            "description":
                            "Tender green beans smoked with bacon and spices.",
                            "piece": ["individual", "family"],
                            "price": [3.0, 5.0],
                            "premium": True
                        }
                    }
                },
                "drinks": {
                    "name": "Drinks",
                    "part_of_meal": True,
                    "meal_step": 3,
                    "item": {
                        "fountain_drink": {
                            "name": "Fountain Drink",
                            "description":
                            "Choose from a variety of refreshing beverages. Options available: lemonade, Coke, Sprite, and Dr. Pepper.",
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
                            "description":
                            "A gallon of refreshing iced tea, sweet or unsweetened.",
                            "piece": ["gallon_sweet", "gallon_unsweet"],
                            "price": [5.0, 5.0]
                        },
                        "fruit_juice": {
                            "name": "Fruit Juice",
                            "description":
                            "A carton of fruit juice, apple or orange.",
                            "piece": ["packaged_apple", "packaged_orange"],
                            "price": [3.0]
                        },
                        "bottled_water": {
                            "name": "Bottled Water",
                            "description": "The original thirst quencher.",
                            "piece": ["packaged"],
                            "price": [0.0]
                        }
                    }
                },
                "desserts": {
                    "name": "Desserts",
                    "part_of_meal": True,
                    "meal_step": 4,
                    "item": {
                        "cookie": {
                            "name":
                            "Cookie",
                            "description":
                            "A freshly baked cookie, available in chocolate chip, oatmeal raisin, or sugar.",
                            "piece": [
                                "chocolate chip", "oatmeal raisin",
                                "sugar"
                            ],
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
                            "description":
                            "A slice of classic apple pie with a flaky crust.",
                            "piece": ["individual"],
                            "price": [4.0]
                        },
                        "cheesecake": {
                            "name": "Cheesecake",
                            "description":
                            "A slice of creamy cheesecake with a graham cracker crust.",
                            "piece": ["individual"],
                            "price": [4.0]
                        },
                        "cobbler": {
                            "name": "Cobbler",
                            "description":
                            "A square of warm cobbler with a buttery crust, available with peach or blackberry.",
                            "piece":
                            ["peach", "blackberry"],
                            "price": [4.0, 4.0]
                        }
                    }
                },
                "combos": {
                    "name": "Combos",
                    "part_of_meal": False,
                    "item": {
                        "mix_tender_combo": {
                            "name": "Mix & Match Combo",
                            "description":
                            "Save 5% on a bucket of tenders with light and dark meat mixed and matched.",
                            "mix_match_rule":
                            "You must pick in sets of 2 tenders between light or dark meat.",
                            "mix_increment": 2,
                            "piece": [10, 12],
                            "price": [20.0, 24.0],
                            "flavor": ["Cajun", "Spicy", "Classic", "Grilled"]
                        },
                        "tender_combo": {
                            "name": "Tenders Combo",
                            "description":
                            "Save 5% on a 4/6pc bucket of tenders with light or dark meat.",
                            "piece": [4, 6],
                            "price": [8.0, 12.0],
                            "dark_or_light": True,
                            "combo_discount": 0.05
                        }
                    }
                },
                "meals": {
                    "name": "Meals",
                    "part_of_meal": False,
                    "item": {
                        "regular_meal": {
                            "name": "Regular Meal",
                            "description":
                            "1 entree, 1 side, 1 drink, and 1 dessert - Save 10%!",
                            "piece": [1],
                            "price": [0.0],
                            "requirements": {
                                "entrees": 1,
                                "sides": 1,
                                "drinks": 1,
                                "desserts": 1
                            },
                            "discount": 0.10
                        },
                        "large_meal": {
                            "name": "Large Meal",
                            "description":
                            "1 entree, 2 sides, 1 drink, and 1 dessert - Save 15%!",
                            "piece": [1],
                            "price": [0.0],
                            "requirements": {
                                "entrees": 1,
                                "sides": 2,
                                "drinks": 1,
                                "desserts": 1
                            },
                            "discount": 0.15
                        }
                    }
                }
            }
        }

        self.create_start_screen()

    def run(self):
        self.main_window.mainloop()

    # Helper Functions
    def switch_frame(self, frame):
        if self.current_frame == frame:  # If the frame is already displayed, do nothing
            return
        if self.current_frame:  # If there's a current frame, destroy it
            self.current_frame.destroy()
        self.current_frame = frame  # Set the new frame as current
        self.current_frame.pack()  # Display the new frame

    def create_start_screen(self):
        # this is the welcome screen
        frame = tk.Frame(self.container)

        welcome_label = tk.Label(frame,
                                 text="Welcome",
                                 font=self.FONT_SIZES["xl"])
        welcome_label.pack(pady=(20, 0))
        welcome_label2 = tk.Label(frame,
                                    text="to Calhoun Fried Chicken!",
                                    font=self.FONT_SIZES["lg"])
        welcome_label2.pack(pady=(0, 20))

        instructions = tk.Label(
            frame,
            text="Start your order by clicking the button below.",
            font=self.FONT_SIZES["md"])
        instructions.pack(pady=10)

        start_button = tk.Button(frame,
                                 text="Start Order",
                                 command=self.create_category_screen,
                                 font=self.FONT_SIZES["md"],
                                 width=30,
                                 height=5)
        start_button.pack(side=tk.BOTTOM, pady=10)

        self.switch_frame(frame)

    def create_category_screen(self):
        # This screen shows all the categories.
        # If a meal is being built and the user hits
        # Back to Categories, ask the user if they want to cancel it.
        if self.meal_builder is not None:
            cancel = messagebox.askyesno(
                "Cancel Meal",
                "You are currently building a meal. Navigating away will cancel your current meal. Do you want to cancel it?"
            )
            if not cancel:  # If the user doesn't want to cancel, return
                return
            else:
                self.meal_builder = None  # Reset the meal builder if the user confirms exiting it.

        frame = tk.Frame(self.container)
        title = tk.Label(frame,
                         text="Select a category",
                         font=self.FONT_SIZES["lg"])
        title.pack(pady=20)

        button_frame = tk.Frame(frame)
        button_frame.pack()

        # Get all category keys.
        category_keys = self.menu["category"].keys()

        # Loop through categories and arrange them in a grid w names
        for i, cat_key in enumerate(category_keys):
            row, col = divmod(i, 2)
            cat_data = self.menu["category"][cat_key]
            display_name = cat_data.get("name", cat_key)

            # Create category button
            category_button = tk.Button(
                button_frame,
                text=display_name,
                command=lambda k=cat_key: self.category_selected(k),
                font=self.FONT_SIZES["md"],
                width=20,
                height=5)
            category_button.grid(row=row, column=col, padx=10, pady=10)

        cart_frame = tk.Frame(frame)
        cart_frame.pack(pady=15)

        # Pack "View Cart" and "Back" buttons so the user
        # can see what they put in the cart from category
        # and they can leave the category
        cart_button = tk.Button(cart_frame,
                                text="View Cart",
                                command=self.view_cart,
                                font=self.FONT_SIZES["md"],
                                width=15)
        cart_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(frame,
                                text="Back",
                                command=self.create_start_screen,
                                font=self.FONT_SIZES["md"])
        back_button.pack(pady=10)

        self.switch_frame(frame)

    def category_selected(self, category_key):

        # if the category is not in the menu then show some message
        # saying "it's coming soon!," and just go back to the category screen
        if category_key in self.menu["category"]:
            display_name = self.menu["category"][category_key]["name"]
            self.create_item_screen(category_key, display_name)
        else:
            frame = tk.Frame(self.container)
            tk.Label(frame,
                     text=f"Category: {category_key}",
                     font=self.FONT_SIZES["lg"]).pack(pady=20)
            tk.Label(frame,
                     text="This category is coming soon!",
                     font=self.FONT_SIZES["md"]).pack(pady=10)
            tk.Button(frame,
                      text="Back",
                      command=self.create_category_screen,
                      font=self.FONT_SIZES["md"]).pack(pady=10)
            self.switch_frame(frame)

    def create_item_screen(self, category_key, display_name):
        # This function is for populating the items from a category passed in on the GUI
        frame = tk.Frame(self.container)

        # Big label for the category name
        tk.Label(frame, text=display_name,
                 font=self.FONT_SIZES["xl"]).pack(pady=10)

        # Check if the category is valid before moving on
        if category_key not in self.menu["category"]:
            messagebox.showerror("Error", f"Invalid category: {category_key}")
            self.create_category_screen()
            return

        # Get all the items in the category
        items = self.menu["category"][category_key]["item"]

        # Now we will loop through them and create a frame in a card-like fashion
        for item_key, item_data in items.items():
            item_container = tk.Frame(frame,
                                      bd=2,
                                      relief=tk.RIDGE,
                                      padx=10,
                                      pady=10)
            item_container.pack(pady=5, fill=tk.X)

            # Some of the sides are premium, so we need to check for that
            # and then append the names with premium.
            item_name = self.get_item_name_with_premium(item_data)
            tk.Label(item_container,
                     text=item_name,
                     font=self.FONT_SIZES["md"],
                     anchor=tk.W).pack(anchor=tk.W)
            tk.Label(item_container,
                     text=item_data["description"],
                     font=self.FONT_SIZES["sm"],
                     wraplength=600,
                     anchor=tk.W).pack(anchor=tk.W)

            # If the item is a "combo" or a "meal," we need to handle it differently.
            if item_data["name"] in ["Regular Meal", "Large Meal"]:

                # For meals, we need to start the meal builder.
                # If the name is "Regular Meal," we need to set the meal type to "regular"
                # else we set it to "large"
                # It's a bit hacky, because we could just check the key, but this is good enough for now.
                meal_type = "regular" if item_data["name"] == "Regular Meal" else "large"
                tk.Button(item_container,
                          text="Select",
                          command=lambda meal_type=meal_type: self.
                          start_meal_builder(meal_type),
                          font=self.FONT_SIZES["md"]).pack(anchor=tk.E)
            # If it's a mix and match then it's even more special, because we have some extra
            # data to pass in.
            elif item_data["name"] == "Mix & Match Combo":
                tk.Button(item_container,
                          text="Customize",
                          command=lambda item_data=item_data: self.
                          create_mix_match_combo_screen(item_data),
                          font=self.FONT_SIZES["md"]).pack(anchor=tk.E)
            # Otherwise, we just create a button to select that item.
            else:
                tk.Button(
                    item_container,
                    text="Select",
                    command=lambda item_key=item_key, category_key=
                    category_key: self.item_selected(category_key, item_key),
                    font=self.FONT_SIZES["md"]).pack(anchor=tk.E)

        # Complementary escape button to go back to the category screen.
        tk.Button(frame,
                  text="Back to Categories",
                  command=self.create_category_screen,
                  font=self.FONT_SIZES["md"]).pack(side=tk.BOTTOM, pady=15)
        self.switch_frame(frame)


    def item_selected(self, category_key, item_key):
        # This function is for populating the screen for an item that the user selected
        # with the item's data, like pc count (size), flavors and meat type, etc.

        # We get all the data in that particular item
        item_data = self.menu["category"][category_key]["item"][item_key]

        frame = tk.Frame(self.container)

        # Label for name and description.
        tk.Label(frame, text=item_data["name"],
                 font=self.FONT_SIZES["xl"]).pack(pady=10)
        tk.Label(frame,
                 text=item_data["description"],
                 font=self.FONT_SIZES["md"],
                 wraplength=500).pack(pady=5)

        # Create a frame for the item options (size, flavor, etc.)
        # It's a helper function that creates a frame for the item options.
        options_frame = self.create_item_options_frame(frame, item_data)
        options_frame.pack(pady=10, fill=tk.X)

        # Add a button to add the item to the cart
        tk.Button(frame,
                  text="Add to Cart",
                  command=lambda: self.handle_add_to_cart(
                      category_key, item_key, options_frame),
                  font=self.FONT_SIZES["md"]).pack(pady=20)

        # Button to go back to the category screen
        tk.Button(
            frame,
            text="Back to Items",
            command=lambda: self.create_item_screen(
                category_key, self.menu["category"][category_key]["name"]),
            font=self.FONT_SIZES["md"]).pack(pady=10)

        self.switch_frame(frame)

    def create_item_options_frame(self, frame, item_data):
        # This is the function that we called earlier for item options
        # to be handled a little more neatly and to be more readable
        options_frame = tk.Frame(frame)
        options_frame.pack(pady=10, fill=tk.X)

        # Variables to hold user selections.
        # StringVar() is used for text variables in Tkinter apparently.
        options_frame.selected_size = tk.StringVar()
        options_frame.selected_flavor = tk.StringVar()
        options_frame.selected_meat_type = tk.StringVar()

        # Create size, flavor, and meat type selections.
        # All helper functions that create the frames for each selection.
        self.create_size_selection(options_frame, item_data)
        self.create_flavor_selection(options_frame, item_data)
        self.create_meat_selection(options_frame, item_data)

        # Now we just return that.
        return options_frame

    def create_size_selection(self, options_frame, item_data):
        # This function creates the frame in the item screen
        # for selecting size/quantity/pc.

        # If pc/size/qty *key* in the dictionary is in the item' data
        # and there is a value on it, then we create a frame for it.
        if "piece" in item_data and len(item_data["piece"]) > 0:
            size_frame = tk.LabelFrame(options_frame,
                                       text="Select Size/Quantity",
                                       padx=10,
                                       pady=10)
            size_frame.pack(fill=tk.X, padx=10, pady=5)

            # Loop through the pieces and prices and create a radio button
            for i, (piece, price) in enumerate(
                    zip(item_data["piece"], item_data["price"])):
                text = self.format_piece_label(piece, price)
                tk.Radiobutton(size_frame,
                               text=text,
                               variable=options_frame.selected_size,
                               value=str(i),
                               font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options_frame.selected_size.set("0") # This is for the default radio pick.

    def create_flavor_selection(self, options_frame, item_data):
        # This function creates the frame in the item screen for flavor

        # Again, if the flavor key in the item data is in the dictionary
        # and there is a value(s) on it, then we create a frame for it.
        if "flavor" in item_data and len(item_data["flavor"]) > 0:
            flavor_frame = tk.LabelFrame(options_frame,
                                         text="Select Flavor",
                                         padx=10,
                                         pady=10)
            flavor_frame.pack(fill=tk.X, padx=10, pady=5)

            # For each flavor, make that radio button.
            for i, flavor in enumerate(item_data["flavor"]):
                tk.Radiobutton(flavor_frame,
                               text=flavor,
                               variable=options_frame.selected_flavor,
                               value=str(i),
                               font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options_frame.selected_flavor.set("0")

    def create_meat_selection(self, options_frame, item_data):
        # This function creates the frame in the item screen for light or dark meat

        # If key in item data and has value then we create a frame for it
        if "dark_or_light" in item_data and item_data["dark_or_light"]:
            meat_frame = tk.LabelFrame(options_frame,
                                       text="Select Meat Type",
                                       padx=10,
                                       pady=10)
            meat_frame.pack(fill=tk.X, padx=10, pady=5)

            # We don't use a `for` loop here because we *know* it's just two.
            tk.Radiobutton(meat_frame,
                           text="Light Meat (white meat, breast and wing)",
                           variable=options_frame.selected_meat_type,
                           value="light",
                           font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            tk.Radiobutton(meat_frame,
                           text="Dark Meat (dark meat, thigh and leg)",
                           variable=options_frame.selected_meat_type,
                           value="dark",
                           font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
            options_frame.selected_meat_type.set("light")

    def handle_add_to_cart(self, category_key, item_key, options_frame):
        # This is a helper function that handles the add to cart button
        # We have this instead of just using a consolidated function
        # `add_to_cart` because we need to do some extra stuff around
        # meals. Combos get their own function like this.
        try:
            flavor_index = int(options_frame.selected_flavor.get(
            )) if options_frame.selected_flavor.get() else None
            meat_type = options_frame.selected_meat_type.get()
            size_index = int(options_frame.selected_size.get()
                             ) if options_frame.selected_size.get() else 0
            item_details = {
                "category": category_key,
                "item_key": item_key,
                "size_index": size_index,
                "flavor_index": flavor_index,
                "meat_type": meat_type,
                "quantity": 1
            }

            # Check if we're in a meal building process
            if self.meal_builder is not None and category_key in [
                    "entrees", "sides", "drinks", "desserts"
            ]:
                self.select_meal_item(item_key, item_details)
            else:
                self.add_to_cart(item_details)

        # Extra stuff to catch errors (I got tired of having to constantly
        # restart the program when I was debugging. It lets me move on to try more
        # quick attempts at breaking it.)
        except ValueError:
            messagebox.showerror("Error", "Please select a valid size.")
        except TypeError as e:
            messagebox.showerror(
                "Error",
                f"Failed to add item to cart due to invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Combos handling
    def create_mix_match_combo_screen(self, item_data):
        # This function is for the mix and match combo screen.
        # We need this, because we have to do some extra stuff
        # around the division of light to dark meat.
        frame = tk.Frame(self.container)

        # Name and description
        tk.Label(frame, text=item_data["name"],
                 font=self.FONT_SIZES["xl"]).pack(pady=10)
        tk.Label(frame,
                 text=item_data["description"],
                 font=self.FONT_SIZES["md"],
                 wraplength=500).pack(pady=5)

        # All the options for the mix and match combo
        options_frame = tk.Frame(frame)
        options_frame.pack(pady=10, fill=tk.X)

        # Tkinter string variables to track selections.
        total_var = tk.StringVar()

        # We're doing IntVar() here because we need to use the slider.
        # It's at 0 by default, so basically all dark meat to the left.
        light_var = tk.IntVar(value=0)
        flavor_var = tk.StringVar()

        # This is if the user changes the pc count in the middle of the
        # combo selection. We need to update the slider to reflect that
        def update_slider():
            new_value = int(total_var.get())
            slider.config(to=new_value)
            slider.set(0)

        # Create section for selecting total pieces
        piece_frame = tk.LabelFrame(options_frame,
                                    text="Select Size/Quantity",
                                    padx=10,
                                    pady=10)
        piece_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create radio buttons for each piece option
        options = [(f"{piece} pc", str(piece)) for piece in item_data["piece"]]
        for text, value in options:
            tk.Radiobutton(piece_frame,
                           text=text,
                           variable=total_var,
                           value=value,
                           font=self.FONT_SIZES["md"],
                           command=update_slider).pack(anchor=tk.W)
        total_var.set(str(item_data["piece"][0]))

        # Create section for light vs dark meat selection
        mix_frame = tk.LabelFrame(options_frame,
                                  text="Light vs Dark Tenders",
                                  padx=10,
                                  pady=10)
        mix_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(mix_frame,
                 text="Light meat ↔ Dark meat",
                 font=self.FONT_SIZES["md"]).pack(anchor=tk.W)

        # Create slider for selecting light vs dark meat ratio
        slider = tk.Scale(mix_frame,
                          variable=light_var,
                          from_=0,
                          to=int(total_var.get()),
                          resolution=item_data.get("mix_increment", 2),
                          orient=tk.HORIZONTAL,
                          font=self.FONT_SIZES["md"])
        slider.pack(fill=tk.X)

        # Create section for flavor selection
        flavor_frame = tk.LabelFrame(options_frame,
                                     text="Select Flavor",
                                     padx=10,
                                     pady=10)
        flavor_frame.pack(fill=tk.X, padx=10, pady=5)
        flavor_options = [(flavor, flavor) for flavor in item_data["flavor"]]
        for text, value in flavor_options:
            tk.Radiobutton(flavor_frame,
                           text=text,
                           variable=flavor_var,
                           value=value,
                           font=self.FONT_SIZES["md"]).pack(anchor=tk.W)
        flavor_var.set(item_data["flavor"][0])

        def handle_add_to_cart():
            try:
                # Dividing the chicken tenders into light and dark
                total_tenders = int(total_var.get())
                light_tenders = light_var.get()
                flavor = flavor_var.get()

                # Item details for the cart
                item_details = {
                    "category": "combos",
                    "item_key": "mix_tender_combo",
                    "total_tenders": total_tenders,
                    "light_tenders": light_tenders,
                    "flavor": flavor
                }
                self.add_to_cart(item_details)

            # Makes debugging easier, lets me break things quick!
            # Debug tool handles throwing exception tracebacks.
            except Exception as e:
                messagebox.showerror("Error",
                                     f"Failed to add item to cart: {e}")

        # Add to cart and back buttons
        tk.Button(frame,
                  text="Add to Cart",
                  command=handle_add_to_cart,
                  font=self.FONT_SIZES["md"]).pack(pady=20)
        tk.Button(frame,
                  text="Back to Items",
                  command=self.create_category_screen,
                  font=self.FONT_SIZES["md"]).pack(pady=10)
        self.switch_frame(frame)

    # Meals handling
    def start_meal_builder(self, meal_type):
        # This function is for starting the meal builder.
        # We need to check if the meal type is valid and then
        # get the first step in the meal builder.
        # We also need to check if the meal type is in the menu.

        if meal_type not in ["regular", "large"]:
            messagebox.showerror(
                "Error",
                "Invalid meal type selected. Please choose 'regular' or 'large'."
            )
            return

        first_step = self.get_first_meal_step()
        if not first_step:
            messagebox.showerror("Error",
                                 "No meal steps found in menu structure.")
            return

        self.meal_builder = {
            "type": meal_type,
            "step": first_step,
            "selections": {},
        }

        self.create_item_screen(first_step,
                                self.menu["category"][first_step]["name"])
        messagebox.showinfo(
            "Building Meal",
            f"Select from {self.menu['category'][first_step]['name']} for your {meal_type.capitalize()} Meal."
        )

    def get_first_meal_step(self):
        # This function gets the first step in the meal builder.
        # We need to check if the `meal_step` is 1 and part_of_meal (boolean).
        first_step = None
        for cat_key, cat_data in self.menu["category"].items():
            if cat_data.get("part_of_meal") and cat_data.get("meal_step") == 1:
                first_step = cat_key
        return first_step

    def select_meal_item(self, item_key, item_details):
        # This function is for selecting an item in the meal builder
        current_step = self.meal_builder["step"]
        self.meal_builder["selections"][current_step] = item_key

        # Store item details for meal components
        if current_step not in self.meal_builder:
            self.meal_builder[current_step] = {}
        self.meal_builder[current_step][item_key] = item_details

        self.advance_meal_step()

    def advance_meal_step(self):
        # This function advances the meal builder to the next step
        # It handles the special case of large meals needing 2 sides
        current_category = self.meal_builder["step"]
        try:
            current_step_number = self.menu["category"][current_category][
                "meal_step"]

            # Special handling for large meals which need 2 sides.
            if current_category == "sides" and self.meal_builder[
                    "type"] == "large":
                if "sides_1" not in self.meal_builder["selections"]:
                    # First side selection - move it to sides_1
                    first_side = self.meal_builder["selections"].pop("sides")
                    self.meal_builder["selections"]["sides_1"] = first_side
                    self.meal_builder["step"] = "sides"
                    self.create_item_screen(
                        "sides", self.menu["category"]["sides"]["name"])
                    messagebox.showinfo(
                        "Second Side",
                        "Please select a second side for your Large Meal.")
                    return
                else:
                    # Second side selection - store it and move to next step.
                    second_side = self.meal_builder["selections"].pop("sides")
                    self.meal_builder["selections"]["sides_2"] = second_side
                    next_step = self.get_next_meal_step(current_step_number)
                    if next_step:
                        self.meal_builder["step"] = next_step
                        self.create_item_screen(
                            next_step,
                            self.menu["category"][next_step]["name"])
                        messagebox.showinfo(
                            "Next Step",
                            f"Select an {self.menu['category'][next_step]['name']} for your {self.meal_builder['type'].capitalize()} Meal."
                        )
                    else:
                        self.finalize_meal_combo()
                    return

            # Normal meal step progression for regular meals.
            next_step = self.get_next_meal_step(current_step_number)
            if next_step:
                self.meal_builder["step"] = next_step
                self.create_item_screen(
                    next_step, self.menu["category"][next_step]["name"])
                messagebox.showinfo(
                    "Next Step",
                    f"Select an {self.menu['category'][next_step]['name']} for your {self.meal_builder['type'].capitalize()} Meal."
                )
            else:
                # If no next step, finalize the meal.
                self.finalize_meal_combo()

        # Error handling.
        except KeyError:
            messagebox.showerror("Error", "Invalid meal step or category.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def get_next_meal_step(self, current_step_number):
        # Find next step by looping through categories
        for step in range(current_step_number + 1, 5): # Meal steps go from 1-4
            for cat_key, cat_data in self.menu["category"].items():
                # If category is part of meal and matches next step number, return it.
                if cat_data.get("part_of_meal") and cat_data.get("meal_step") == step:
                    return cat_key
        return None

    def finalize_meal_combo(self):
        # This function finalizes a meal combo by checking if all required items
        # are selected and then adding it to the cart with the appropriate discount
        try:
            # Get the meal type (regular or large) and its corresponding key
            meal_type = self.meal_builder["type"]
            meal_key = self.MEAL_DISCOUNT_KEYS[meal_type]
            meal_data = self.menu["category"]["meals"]["item"][meal_key]
            required_items = meal_data["requirements"]
            selected_items = self.meal_builder["selections"]

            # Check if all required items are selected (basically error handling)
            if not self.check_meal_eligibility(required_items, selected_items):
                messagebox.showerror(
                    "Error",
                    f"Your {meal_type.capitalize()} Meal is missing required items."
                )
                return

            # Prepare component items with their details
            component_items_with_details = {}
            for category, item_key in selected_items.items():
                # Determine the actual category for accessing menu data
                actual_category = category
                # If category is sides_1 or sides_2, map it to sides
                if category in ["sides_1", "sides_2"]:
                    actual_category = "sides"

                # Get component details from the meal builder
                # This includes things like size, flavor, meat type
                details = {}
                if actual_category in self.meal_builder and item_key in self.meal_builder[
                        actual_category]:
                    details = self.meal_builder[actual_category][item_key]

                # Store the component details
                component_items_with_details[category] = {
                    "item_key": item_key,
                    "details": details
                }

            # Create the details for the meal to be added to cart
            item_details = {
                "category": "meals",
                "item_key": meal_key,
                "component_items": component_items_with_details,
                "quantity": 1
            }

            # Clear the meal builder after adding to cart
            self.add_to_cart(item_details)
            self.meal_builder = None

            # Return to category screen after adding meal to cart
            self.create_category_screen()

        # Error handling for meal building issues
        except KeyError as e:
            messagebox.showerror("Error",
                                 f"Invalid meal type or item key: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def check_meal_eligibility(self, required_items, selected_items):
        for category in required_items:  # Iterate over keys, not items.
            if category == "sides" and self.meal_builder["type"] == "large":
                if not ("sides_1" in selected_items and "sides_2" in selected_items):
                    return False
            elif category not in selected_items:
                return False
        return True

    def add_to_cart(self, item_details):
        # This function is for adding items to the cart with proper pricing
        try:
            category_key = item_details["category"]
            item_key = item_details["item_key"]

            # Convert sides_1 and sides_2 to sides for meal components
            if category_key in ["sides_1", "sides_2"]:
                category_key = "sides"

            # Get item data from menu
            item_data = self.menu["category"][category_key]["item"][item_key]
            quantity = item_details.get("quantity", 1)

            # Handle pricing for different item types
            if category_key == "meals":
                # For meals, sum up component prices and apply discount
                price = 0.0
                for component_category_key, component_data in item_details["component_items"].items():
                    component_item_key = component_data["item_key"]
                    # Map sides_1/sides_2 to sides category
                    actual_category = "sides" if component_category_key in ["sides_1", "sides_2"] else component_category_key
                    component_item_data = self.menu["category"][actual_category]["item"][component_item_key]
                    price += self.get_first_price(component_item_data)
                discount = item_data["discount"]
                price *= (1 - discount)
            elif category_key == "combos" and item_key == "mix_tender_combo":
                # For mix & match combos, get price based on total tenders
                price = self.get_item_price(category_key, item_key,
                    item_data["piece"].index(item_details["total_tenders"]))
            elif category_key == "combos" and item_key == "tender_combo":
                # For regular combos, get price based on size index
                price = self.get_item_price(category_key, item_key, item_details["size_index"])
            else:
                # For regular items, get price based on size index
                price = self.get_item_price(category_key, item_key, item_details["size_index"])

            # Add specified quantity of items to cart
            for _ in range(quantity):
                cart_item = {
                    "category": category_key,
                    "item_key": item_key,
                    "price": price,
                }
                # Add any additional item details
                cart_item.update({
                    k: v
                    for k, v in item_details.items()
                    if k not in ["category", "item_key", "quantity"]
                })
                self.cart.append(cart_item)

            # Show success message
            messagebox.showinfo("Success", f"{quantity} {item_data['name']} added to cart.")

            # Return to category screen after adding item
            self.create_category_screen()

        # Error handling
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid item or category key: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_cart_summary(self, parent_frame):
        # Shows what's in your cart with prices and discounts
        subtotal = 0  # Running total before taxes
        total_discount = 0  # Total money saved from discounts

        for item in self.cart:
            # Get basic info about the item
            item_data = self.menu["category"][item["category"]]["item"][item["item_key"]]
            original_price = item["price"]
            quantity = item.get("quantity", 1)

            # Handle combo items (5% off)
            if item["category"] == "combos":
                discounted_price = original_price  # Price after discount
                original_price = discounted_price / (1 - self.COMBO_DISCOUNT)  # Work backwards to get original
                discount_amount = original_price - discounted_price
                total_discount += discount_amount * quantity

                # Show combo item details on screen
                tk.Label(parent_frame, text=f"{item_data['name']}", font=self.FONT_SIZES["md"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Original Price: ${original_price:.2f}", font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Combo Discount ({self.COMBO_DISCOUNT * 100:.0f}%): -${discount_amount:.2f}",
                        font=("Comic Sans MS", 10, "italic"), fg="green", anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Final Price: ${discounted_price:.2f}", font=self.FONT_SIZES["md"], anchor=tk.W).pack(fill=tk.X)
                subtotal += discounted_price * quantity

            # Handle meal items (10% or 15% off)
            elif item["category"] == "meals":
                discount = item_data["discount"]
                original_price = original_price / (1 - discount)  # Work backwards to get original
                discount_amount = original_price - item["price"]
                total_discount += discount_amount * quantity

                # Show meal item details on screen
                tk.Label(parent_frame, text=f"{item_data['name']}", font=self.FONT_SIZES["md"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Original Price: ${original_price:.2f}", font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Meal Discount ({discount * 100:.0f}%): -${discount_amount:.2f}",
                        font=("Comic Sans MS", 10, "italic"), fg="green", anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"  Final Price: ${item['price']:.2f}", font=self.FONT_SIZES["md"], anchor=tk.W).pack(fill=tk.X)
                subtotal += item["price"] * quantity

            # Handle regular items (no discount)
            else:
                tk.Label(parent_frame, text=f"{item_data['name']} - ${original_price:.2f}",
                        font=self.FONT_SIZES["md"], anchor=tk.W).pack(fill=tk.X)
                subtotal += original_price * quantity

            # Show how many of this item ordered
            tk.Label(parent_frame, text=f"Quantity: {quantity}",
                    font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Show size if item has one
            if item.get("size_index") is not None:
                tk.Label(parent_frame, text=f"Size: {self.get_size_text(item_data, item['size_index'])}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Show flavor if item has one
            if item.get("flavor_index") is not None:
                tk.Label(parent_frame, text=f"Flavor: {self.get_flavor_text(item_data, item['flavor_index'])}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Show meat type if item has one
            if item.get("meat_type") is not None and "dark_or_light" in item_data and item_data["dark_or_light"]:
                tk.Label(parent_frame, text=f"Meat Type: {self.get_meat_text(item['meat_type'])}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Show tender details if mix & match combo
            if item.get("total_tenders") is not None:
                tk.Label(parent_frame, text=f"Total Tenders: {item['total_tenders']}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"Light Tenders: {item['light_tenders']}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                tk.Label(parent_frame, text=f"Flavor: {item['flavor']}",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Show meal components if it's a meal
            if item.get("component_items") is not None:
                tk.Label(parent_frame, text=f"Meal Components:",
                        font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                for component_category, component_data in item["component_items"].items():
                    component_item_key = component_data["item_key"]
                    # Fix category name for sides
                    actual_category = "sides" if component_category in ["sides_1", "sides_2"] else component_category
                    component_item_data = self.menu["category"][actual_category]["item"][component_item_key]

                    # Show component name
                    tk.Label(parent_frame, text=f"  - {component_item_data['name']}",
                            font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

                    # Show component details if any exist
                    if component_data["details"]:
                        if component_data["details"].get("size_index") is not None:
                            tk.Label(parent_frame,
                                    text=f"    Size: {self.get_size_text(component_item_data, component_data['details']['size_index'])}",
                                    font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                        if component_data["details"].get("flavor_index") is not None:
                            tk.Label(parent_frame,
                                    text=f"    Flavor: {self.get_flavor_text(component_item_data, component_data['details']['flavor_index'])}",
                                    font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)
                        if component_data["details"].get("meat_type") is not None and "dark_or_light" in component_item_data and component_item_data["dark_or_light"]:
                            tk.Label(parent_frame,
                                    text=f"    Meat Type: {self.get_meat_text(component_data['details']['meat_type'])}",
                                    font=self.FONT_SIZES["sm"], anchor=tk.W).pack(fill=tk.X)

            # Add a line between items
            tk.Label(parent_frame, text="─" * 50, anchor=tk.W).pack(fill=tk.X)

        return subtotal, total_discount

    def view_cart(self):
        # Make a new screen to show cart
        frame = tk.Frame(self.container)
        tk.Label(frame, text="Your Cart", font=self.FONT_SIZES["xl"]).pack(pady=10)

        # Make cart scrollable when it gets big
        container = tk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container, height=400)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Make scroll area adjust when content changes
        scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Show message if cart empty, otherwise show items
        if not self.cart:
            tk.Label(scrollable_frame, text="Your cart is empty.",
                    font=self.FONT_SIZES["md"]).pack(pady=10)
        else:
            # Show all items and calculate totals
            subtotal, total_discount = self.display_cart_summary(scrollable_frame)
            totals_frame = tk.Frame(frame)
            totals_frame.pack(fill=tk.X, pady=10)

            # Show pricing breakdown
            tk.Label(totals_frame, text=f"Subtotal: ${subtotal:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            tk.Label(totals_frame, text=f"Total Discount: -${total_discount:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            tax = (subtotal - total_discount) * self.TAX_RATE
            tk.Label(totals_frame, text=f"Tax ({self.TAX_RATE * 100:.0f}%): ${tax:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            total = subtotal - total_discount + tax
            tk.Label(totals_frame, text=f"Total: ${total:.2f}",
                    font=self.FONT_SIZES["lg"]).pack(pady=10)

            # Add checkout button
            tk.Button(totals_frame, text="Checkout", command=self.checkout,
                     font=self.FONT_SIZES["md"]).pack(pady=10)

        # Add back button
        tk.Button(frame, text="Back to Categories", command=self.create_category_screen,
                 font=self.FONT_SIZES["md"]).pack(pady=10)
        self.switch_frame(frame)

    def checkout(self):
        # Make checkout screen
        frame = tk.Frame(self.container)
        tk.Label(frame, text="Checkout", font=self.FONT_SIZES["xl"]).pack(pady=10)

        # Make checkout scrollable
        container = tk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container, height=400)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Show message if cart empty, otherwise process order
        if not self.cart:
            tk.Label(scrollable_frame, text="Your cart is empty.",
                    font=self.FONT_SIZES["md"]).pack(pady=10)
        else:
            # Show final order details
            subtotal, total_discount = self.display_cart_summary(scrollable_frame)
            totals_frame = tk.Frame(frame)
            totals_frame.pack(fill=tk.X, pady=10)

            # Show final pricing
            tk.Label(totals_frame, text=f"Subtotal: ${subtotal:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            tk.Label(totals_frame, text=f"Total Discount: -${total_discount:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            tax = (subtotal - total_discount) * self.TAX_RATE
            tk.Label(totals_frame, text=f"Tax ({self.TAX_RATE * 100:.0f}%): ${tax:.2f}",
                    font=self.FONT_SIZES["md"]).pack(pady=5)
            total = subtotal - total_discount + tax
            tk.Label(totals_frame, text=f"Total: ${total:.2f}",
                    font=self.FONT_SIZES["lg"]).pack(pady=10)

            # Thank customer and clear cart
            tk.Label(totals_frame, text="Thank you for your order!",
                    font=self.FONT_SIZES["md"]).pack(pady=10)
            # Print cart contents for order tracking/debugging in a formatted way
            print("\n=== ORDER DETAILS ===")
            for item in self.cart:
                print(f"\nItem Category: {item['category']}")
                print(f"Item Key: {item['item_key']}")
                print(f"Price: ${item['price']:.2f}")
                if 'quantity' in item:
                    print(f"Quantity: {item['quantity']}")
                if 'component_items' in item:
                    print("Components:")
                    for comp_cat, comp_data in item['component_items'].items():
                        print(f"  - {comp_cat}: {comp_data['item_key']}")
            print("\n===================")
            print("RAW DATA:")
            print(self.cart)
            print("===================")
            print("Order total: $", total)
            self.cart = []  # Clear cart after checkout

        # Add back button
        tk.Button(frame, text="Back to Start", command=self.create_start_screen,
                 font=self.FONT_SIZES["md"]).pack(pady=10)
        self.switch_frame(frame)

    # ---- MORE HELPER FUNCTIONS ----
    # These functions are used to get item details and format them nicely

    def get_item_price(self, category_key, item_key, size_index=0):
        # Get price of item based on its size
        item_data = self.menu["category"][category_key]["item"][item_key]
        if "price" in item_data and 0 <= size_index < len(item_data["price"]):
            return item_data["price"][size_index]
        return 0.0

    def get_first_price(self, item_data):
        # Get first price in list or 0 if no prices
        return item_data["price"][0] if item_data.get("price") else 0.0

    def get_size_text(self, item_data, size_index):
        # Make size text look nice
        if "piece" not in item_data or size_index >= len(item_data["piece"]):
            return ""
        piece = item_data["piece"][size_index]
        if isinstance(piece, int):
            return f"{piece} pc"
        else:
            return " ".join(word.capitalize() for word in piece.split("_"))

    def get_flavor_text(self, item_data, flavor_index):
        # Get flavor text if it exists
        if "flavor" not in item_data or flavor_index is None or flavor_index >= len(item_data["flavor"]):
            return ""
        return item_data["flavor"][flavor_index]

    def get_meat_text(self, meat_type):
        # Make meat type text look nice
        if not meat_type:
            return ""
        return f"{meat_type.capitalize()} meat"

    def get_item_name_with_premium(self, item_data):
        # Add (Premium) to name if item is premium
        item_name = item_data["name"]
        if "premium" in item_data and item_data["premium"]:
            item_name += " (Premium)"
        return item_name

    def format_piece_label(self, piece, price):
        # Make piece and price text look nice
        if isinstance(piece, int):
            return f"{piece} pc - ${price:.2f}"
        else:
            return f"{piece.capitalize()} - ${price:.2f}"


if __name__ == "__main__":
    app = CalhounFriedChicken()
    app.run()
