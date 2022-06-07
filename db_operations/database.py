from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from configparser import ConfigParser


class DataBase:
    def __init__(self):
        config = ConfigParser()
        config.read('config/config.ini.txt')
        config.sections()
        self.cloud_config = {
            'secure_connect_bundle': config["database"]["path"]
        }
        self.auth_provider = PlainTextAuthProvider(config['database']['clientid'], config['database']['clientsecret'])
        self.session = None

    def connect_db(self):
        """
        Connecting to the database
        """
        try:
            cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
            self.session = cluster.connect()
        except Exception as e:
            raise e

    def insert_data(self, AGE,BMI,SEX,CHILDREN,SMOKER,REGION):

        """
        :param region: region
        :param smoker: smoker
        :param children: children
        :param sex:gender
        :param bmi: bmi
        :param age: age will be entered from ui

test_keyspace is keyspace and tab is table name
        """

        try:
            if self.is_connected():

                data = self.session.prepare(
                    f"INSERT INTO test_keyspace.tab (id,age,bmi,sex,children,smoker,region) VALUES(uuid(),?,?,?,?,?,?)")
                self.session.execute(data, [AGE,BMI,SEX,CHILDREN,SMOKER,REGION])

            else:
                raise Exception('Database not connected')
        except Exception as e :
            raise e



    def create_tables(self):
        """
         table will be created if not exist
        """

        try:
            table = self.session.execute("SELECT * FROM system_schema.tables WHERE keyspace_name= 'test_keyspace' ;")
            if table:
                return
            else:
                self.session.execute(
                    "CREATE TABLE tab (id uuid \
                    age int,bmi int ,sex int,children int, smoker int,region text, PRIMARY KEY(id)) ;")

        except Exception as e:
            raise e

    def read_data(self):
        """
        Read data from database
        :return: retrieved data
        """

        try:
            if self.is_connected():
                data = self.session.execute(f"select * from test_keyspace.tab")
            else:
                raise Exception('Database not connected')
            return data
        except Exception as e:
            raise e

    def is_connected(self):
        """
        Check if database is connected
        :return: True- Connected
                 False- Not Connected
        """

        try:
            if self.session:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def close_connection(self):
        """
        Close database connection
        """

        try:
            if not self.session.is_shutdown:
                self.session.shutdown()
        except Exception as e:
            raise e
