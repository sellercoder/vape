from orator import DatabaseManager, Schema, Model
config = {
    'sqlite3': {
        'driver': 'sqlite',
        'database': '../bot.db',
    }
}

db = DatabaseManager(config)
schema = Schema(db)
Model.set_connection_resolver(db)

class User(Model):
	__timestamps__ = False

class Category(Model):
	__timestamps__ = False

class Good(Model):
	__timestamps__ = False

class Picture(Model):
	__timestamps__ = False












