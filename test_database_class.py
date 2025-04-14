from database import DatabaseThat

my_database = DatabaseThat("token_usage.db")

my_database.open_database()

my_database.show_all_usages()

my_database.calculate_and_store_dollar_prices()

