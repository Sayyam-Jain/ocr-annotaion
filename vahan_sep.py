import os
import shutil
import random
import string
from tqdm import tqdm
import pandas as pd
import xlsxwriter
from PIL import Image

def get_random_string():
	return ''.join(random.choice(string.ascii_uppercase) for i in range(3))


data_dir = '/media/chetan/12BEC130BEC10CE3/Train_OCR_Data/OCR'
plate_dir = os.path.join(data_dir, 'plates')
bikes_dir = os.path.join(data_dir, 'bikes')
cars_dir = os.path.join(data_dir, 'cars')
if not os.path.exists(bikes_dir):
	os.makedirs(bikes_dir)

if not os.path.exists(cars_dir):
	os.makedirs(cars_dir)


df = pd.read_csv(os.path.join(data_dir, 'OCR.csv'))
# print(df.head())
# print(get_random_string())
csv_dict = dict(df.values.tolist())


# Creating Excel Sheet
workbook = xlsxwriter.Workbook('Data.xlsx')
worksheet = workbook.add_worksheet() # Sheet1
worksheet.set_default_row(128)

worksheet.write('A1', 'Image')
worksheet.write('B1', 'OCR')
worksheet.write('C1', 'Path')

write_index = 2
shards = 3000
for index, (image, ocr) in tqdm(enumerate(csv_dict.items())):

	if index%shards==0 and index!=0:
		workbook.close()
		# Creating Excel Sheet
		write_index = 2
		workbook = xlsxwriter.Workbook('Data'+str(index)+'.xlsx')
		worksheet = workbook.add_worksheet() # Sheet1
		worksheet.set_default_row(128)

		worksheet.write('A1', 'Image')
		worksheet.write('B1', 'OCR')
		worksheet.write('C1', 'Path')

	name = None
	try:
		new_name = ocr + '_' + get_random_string() + '.jpg'
		if 'auto' in image or 'twowheeler' in image:
			name = os.path.join(bikes_dir, new_name)
			
		else:
			name = os.path.join(cars_dir, new_name)
		
		if name is not None:
			plate_path = os.path.join(plate_dir, image)
			img_h, img_w = Image.open(plate_path).size
			shutil.copy(plate_path, name)
			worksheet.insert_image('A' + str(write_index), name)
			worksheet.write('B' + str(write_index), ocr)
			worksheet.write('C' + str(write_index), name)
			write_index+=1
	except Exception as E:
		print(image, E)
		pass
		# print(image, E)
	# if index >= 1500:
	#     break
		
workbook.close()

