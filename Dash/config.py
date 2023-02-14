import os

config = {
	
	'product_types':[
		'toilet paper',
		'soap',
		'hand sanitiser',
		'milk',
		'bread',
		'pasta',
		'tinned food',
		'fresh fruit',
		'fresh vegetables',
	],
	'stocklevel_dict':{
		0:'Out of stock',
		1:'Low stock',
		2:'Medium stock',
		3:'High stock'
	},
	    'store_names':[
        'Sainsburys',
        'Coop',
        'Waitrose',
        'Aldi'
    ],


	'DB_FILEPATH':os.getenv("CSV_FILE", "..flask/db/stock_db.csv"),
	'FLASK_APP_URL':'http://flask-app:5000', # change to fastapi url
}