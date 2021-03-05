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
	__guarded__ = ['created_at', 'updated_at']

class Category(Model):
	__guarded__ = ['created_at', 'updated_at']

class Good(Model):
	__guarded__ = ['created_at', 'updated_at']

class Picture(Model):
	__guarded__ = ['created_at', 'updated_at']













