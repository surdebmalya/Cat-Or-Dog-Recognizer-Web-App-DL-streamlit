import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import shutil

import os # inbuilt module
import random # inbuilt module
import webbrowser # inbuilt module

#=================================== Title ===============================
st.title("""
Cat 🐱 Or Dog 🐶 Recognizer
	""")

#================================= Title Image ===========================
st.text("""""")
img_path_list = ["static\\image_1.jpg",
				"static\\image_2.jpg"]
index = random.choice([0,1])
image = Image.open(img_path_list[index])
st.image(
	        image,
	        use_column_width=True,
	    )

#================================= About =================================
st.write("""
## 1️⃣ About
	""")
st.write("""
Hi all, Welcome to this project. It is a Cat Or Dog Recognizer App!!!
	""")
st.write("""
You have to upload your own test images to test it!!!
	""")
st.write("""
**Or**, if you are too much lazy **(**😎, like me!**)**, then also no problem, we already selected some test images for you, you have to just go to that section & click the **⬇️ Download** button to download those pictures!  
	""")

#============================ How To Use It ===============================
st.write("""
## 2️⃣ How To Use It
	""")
st.write("""
Well, it's pretty simple!!!
- Let me clear first, the model has power to predict image of Cats and Dogs only, so you are requested to give image of a Cat Or a Dog, unless useless prediction can be done!!! 😆 
- First of all, download image of a Cat 🐈 or a Dog 🐕!
- Next, just Browse that file or Drag & drop that file!
- Please make sure that, you are uploading a picture file!
- Press the **👉🏼 Predict** button to see the magic!!!

🔘 **NOTE :** *If you upload other than an image file, then it will show an error massage when you will click the* **👉🏼 Predict** *button!!!*
	""")

#========================= What It Will Predict ===========================
st.write("""
## 3️⃣ What It Will Predict
	""")
st.write("""
Well, it can predict wheather the image you have uploaded is the image of a Cat 🐈 or a Dog 🐕!
	""")

#============================== Sample Images For Testing ==================
st.write("""
## 4️⃣  Download Some Images For Testing!!!
	""")
st.write("""
Hey there! here is some images of Cats & Dogs!
- Here you can find a total of 10 images **[**5 for each category**]**
- Just click on **⬇️ Download** button & download those images!!!
- You can also try your own images!!!
	""")

#============================= Download Button =============================
st.text("""""")
download = st.button("⬇️ Download")

#============================ Download Clicked =============================
if download:
	link = "https://drive.google.com/drive/folders/1i_ukZQxJsCWq2WpISwNa5HFD8smxNdee?usp=sharing"
	try:
		webbrowser.open(link)
	except:
		st.write("""
    		⭕ Something Went Wrong!!! Please Try Again Later!!!
    		""")

#============================ Behind The Scene ==========================
st.write("""
## 5️⃣ Behind The Scene
	""")
st.write("""
To see how it works, please click the button below!
	""")
st.text("""""")
github = st.button("👉🏼 Click Here To See How It Works")
if github:
	github_link = "https://github.com/surdebmalya/Cat-Or-Dog-Recognizer-Web-App-DL-streamlit"
	try:
		webbrowser.open(github_link)
	except:
		st.write("""
    		⭕ Something Went Wrong!!! Please Try Again Later!!!
    		""")

#======================== Time To See The Magic ===========================
st.write("""
## 👁️‍🗨️ Time To See The Magic 🌀
	""")

#========================== File Uploader ===================================
img_file_buffer = st.file_uploader("Upload an image here 👇🏻")

try:
	image = Image.open(img_file_buffer)
	img_array = np.array(image)
	st.write("""
		Preview 👀 Of Given Image!
		""")
	if image is not None:
	    st.image(
	        image,
	        use_column_width=True
	    )
	st.write("""
		Now, you are just one step ahead of prediction.
		""")
	st.write("""
		**Just Click The '👉🏼 Predict' Button To See The Prediction Corresponding To This Image! 😄**
		""")
except:
	st.write("""
		### ❗ Any Picture hasn't selected yet!!!
		""")

#================================= Predict Button ============================
st.text("""""")
submit = st.button("👉🏼 Predict")

#==================================== Model ==================================
def processing(testing_image_path):
    IMG_SIZE = 50
    img = tf.keras.preprocessing.image.load_img(testing_image_path, 
                                                target_size=(IMG_SIZE, IMG_SIZE), color_mode="grayscale")
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array/255.0
    img_array = img_array.reshape((1, 50, 50, 1))   
    prediction =loaded_model.predict(img_array)    
    return prediction

def generate_result(prediction):
	st.write("""
	## 🎯 RESULT
		""")
	if prediction[0]<0.5:
	    st.write("""
	    	## Model predicts it as an image of a CAT 🐱!!!
	    	""")
	else:
	    st.write("""
	    	## Model predicts it as an image of a DOG 🐶!!!
	    	""")

#=========================== Predict Button Clicked ==========================
if submit:
	try:
		# Creating Directory
		not_created = True
		while not_created:
			name_of_directory = random.choice(list(range(0, 1885211)))
			try:
				ROOT_DIR = os.path.abspath(os.curdir)
				if str(name_of_directory) not in os.listdir(ROOT_DIR):
					not_created = False
					path = ROOT_DIR + "\\" + str(name_of_directory)
					os.mkdir(path)
					# directory made!
			except:
				st.write("""
					### ❗ Oops!!! Seems like it will not support in you OS!!!
					""")

		# save image on that directory
		tf.keras.preprocessing.image.save_img(path+"\\test_image.png", img_array)

		image_path = path+"\\test_image.png"
		# Predicting
		st.write("👁️ Predicting...")

		model_path_h5 = "model\\model.h5"
		model_path_json = "model\\model.json"
		json_file = open(model_path_json, 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		loaded_model = tf.keras.models.model_from_json(loaded_model_json)
		loaded_model.load_weights(model_path_h5)

		loaded_model.compile(loss='binary_crossentropy', metrics=['accuracy'],optimizer='adam')

		prediction = processing(image_path)

		# Delete the folder
		dir_path = path
		try:
		    shutil.rmtree(dir_path)
		except:
			pass

		generate_result(prediction)

	except:
		st.write("""
		### ❗ Please Select A Picture First!
			""")

#=============================== Copy Right ==============================
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.text("""""")
st.write("""
### ©️ Created By Debmalya Sur
	""")
