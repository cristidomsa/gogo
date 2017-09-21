import pyqrcode
import zbar
import scipy
import zbar.misc
import scipy.misc

class Barcodes():

	@staticmethod
	def generate(content):
		
		print content

		img = pyqrcode.create(content['string'],
							  error='L', 
							  version=10, 
							  mode='binary')

		img.png('./assets/' + content['path'], scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])

		img.show()

	@staticmethod
	def process(image_filename):
		image = scipy.misc.imread('./assets/uploads/' + image_filename)
		if len(image.shape) == 3:
			image = zbar.misc.rgb2gray(image)

		return image

	@staticmethod
	def decode(image_filename):
		scanner = zbar.Scanner()

		image_as_numpy_array = Barcodes.process(image_filename)

		results = scanner.scan(image_as_numpy_array)

		output = []
		if not results:
			return None
		for result in results:
			output.append((result.type, result.data.decode('ascii'), result.quality))

		return output