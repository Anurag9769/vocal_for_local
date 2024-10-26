# VOCAL FOR LOCAL

PROBLEM STATEMENT:

To identify and analyze the key challenges in the hyperlocal market in India and propose innovative solutions that enhance efficiency of local shop owner to manage their inventory in their local language.

## Table of Contents

- [Installation](#installation)
  ```python
  pip install -r requirement.txt
  
- [Usage](#usage)
  Create a prtostre data base provide the details in the app.py file
  Sample SQL:
  ```sql
    CREATE TABLE public.inventory (
      item_name VARCHAR(100),  
  	mfg_date DATE,  
      expiry_date DATE,                  
      quantity INT,                     
      max_quantity INT,                  
      need_to_purchase BOOLEAN,          
      notes TEXT                         
      );
      INSERT INTO public.inventory (item_name, mfg_date, expiry_date, quantity, max_quantity, need_to_purchase, notes)
      VALUES 
      ('Basmati Rice', '2023-08-15', '2025-08-15', 200, 300, FALSE, 'Premium quality rice'),
      ('Coconut Oil', '2023-09-01', '2025-09-01', 120, 150, FALSE, 'Cold-pressed coconut oil'),
      ('Whole Wheat Atta', '2024-01-10', '2024-11-10', 150, 200, TRUE, 'Organic whole wheat atta'),
      ('Butter', '2024-09-15', '2024-11-20', 40, 60, TRUE, 'Unsalted butter, needs refrigeration'),
      ('Fresh Paneer', '2024-10-05', '2024-10-30', 25, 50, TRUE, 'Fresh paneer from local dairy'),
      ('Green Tea', '2023-06-15', '2025-08-20', 60, 100, FALSE, 'Organic green tea, antioxidant-rich'),
      ('Tomato Ketchup', '2023-12-01', '2025-03-15', 100, 200, FALSE, 'No preservatives added'),
      ('Moong Dal', '2024-03-01', '2025-02-01', 80, 120, TRUE, 'Split moong dal, ready to be restocked'),
      ('Ground Coffee', '2023-05-10', '2025-05-10', 40, 80, TRUE, 'Finely ground premium coffee'),
      ('Pasta', '2024-07-01', '2024-12-01', 200, 250, FALSE, 'Imported Italian pasta');
  ```
  Run the fask application, it will start the chat server which provide response via LLM model by analyssing the provided postgress database connection details
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Anurag9769/vocal_for_local.git
   cd vocal_for_local
