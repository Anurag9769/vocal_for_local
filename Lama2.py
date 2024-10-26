from vanna.vannadb import VannaDB_VectorStore


class MyVanna(VannaDB_VectorStore):
    def __init__(self, model_name):
        super().__init__(vanna_model=model_name)


if __name__ == '__main__':
    # Load the model you created earlier
    vn = MyVanna("lama_inventory_model")

    # Connect to your database
    vn.connect_to_postgres(host='localhost', dbname='postgres', user='postgres', password='Anurag@#', port='5432')

    # Now you can use the loaded model to query, train, or interact
    answer = vn.ask('which item will expire first?')
    print(answer)
    vn.train(
