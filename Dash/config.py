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
        'Sainsburys_Euston',
        'Sainsburys_Holborn',
        'Sainsburys_Soho',
        'Sainsburys_Barbican'
    ],


	'DB_FILEPATH':os.getenv("CSV_FILE", "..FastAPI/app/db/stock_db.csv"),
    'FastAPI_APP_URL':'http://localhost:8000'
}