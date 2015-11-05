import json

def jsonfeed():

	json_list = []

	# for entry in entries:
	idd = 12
	title = 'My event'
	start = '2015-11-05T09:20:22+00:00'
	end = '2015-11-05T13:20:22+00:00'

	json_entry = {'id':idd, 'start':start, 'end':end, 'title': title}

	# print json_entry

	json_list.append(json_entry)

	# print json_list

	

	# Open a file for writing
	out_file = open("test.json","w")

	# Save the dictionary into this file
	# (the 'indent=4' is optional, but makes it more readable)
	json.dump(json_list,out_file, indent=4)                                    

	# Close the file
	out_file.close()


	return json.dumps(json_list)


print jsonfeed()