#importing Ollama, which allows users to connect with any open-source LLM
from vanna.ollama import Ollama
from vanna.vannadb import VannaDB_VectorStore

class MyVanna(VannaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        MY_VANNA_MODEL = 'mumbai_hacks' # Your model name from https://vanna.ai/account/profile
        VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key='6314c5f41d7b4e4e8e865db9456d3002', config=config)
        Ollama.__init__(self, config=config)

if __name__ == '__main__':
    # use llama3:70B for the 70B model
    vn = MyVanna(config={'model': 'llama3'})
    #vn = MyVanna("lama_inventory_model")
    vn.connect_to_postgres(host='localhost', dbname='postgres', user='postgres', password='Anurag@#', port='5432')

    # The information schema query may need some tweaking depending on your database. This is a good starting point.
    #df_information_schema = vn.run_sql("SELECT * FROM mumbai_hacks.inventory")
    #print("DataFrame contents:\n", df_information_schema)  # Check DataFrame contents
    """
    if df_information_schema.empty:
        print("Warning: The DataFrame is empty. Check your SQL query or database connection.")
        # You may want to handle this case differently, e.g., return or raise an error
    """
    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    #plan = vn.train(df_information_schema)
    #plan

    # If you like the plan, then uncomment this and run it to train

    #vn.train(ddl="""
#       CREATE TABLE IF NOT EXISTS mumbai_hacks.inventory
#(
#    item_name character varying(100) COLLATE pg_catalog."default",
#    mfg_date date,
#    expiry_date date,
#    quantity integer,
#    max_quantity integer,
#    need_to_purchase text COLLATE pg_catalog."default",
#    notes text COLLATE pg_catalog."default"
#)
 #   """)

    #vn.train(sql="SELECT * FROM inventory")
    a,b,c = vn.ask('Which item will expire first?')
    print("SQL: ", a)
    print("Result: ", b)
    #success = vn.create_model("lama_inventory_model")


