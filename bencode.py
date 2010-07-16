# bencode.py -- deals with bencoding

# Raised if an error occurs decoding, typically malformed expressions
class DecodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Decode an integer
def decode_int(data):
	try:
		assert data[0] == "i"	# Check it's an integer
		end = data.index('e')	# Find the end of the integer
	except AssertionError:
		raise DecodeError("Badly formed expression.")
	except ValueError:
		raise DecodeError("Cannot find end of expression.")

	# Collapse all the tokens together
	t = reduce(lambda x, y: x + y, data[1:end])

	return int(t)				# Integerise it

# Decode a string
def decode_string(data):
	try:
		assert data[0].isdigit() == True
	except AssertionError:
		raise DecodeError("Badly formed expression.")

	# Work out how long the string is, as the number could be tokened
	num = []
	for x in data:
		if x == ":":
			break
		else:
			num.append(x)
	n = reduce(lambda x, y: x + y, num)
	n = int(n)
	
	# Work out how many digits are at the start
	lenNum = 1	# The number of digits (and the colon)
	for x in data:
		if x.isdigit() == True:
			lenNum += 1
		else:
			break
	
	t = reduce(lambda x, y: x + y, data[lenNum:n+lenNum])
	
	return t