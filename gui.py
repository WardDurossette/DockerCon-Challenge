import Tkinter as tk
import subprocess
import json
import urllib

# Creating GUI
top = tk.Tk()

# Instructions field
def instructionsCallBack():
   tkMessageBox.showinfo( "Hello Docker")
hello = tk.Label(top, height = "3", text = "Hello! Enter the fields to dockerize your pic!")
hello.pack()

# Help window
def helpWindow():
    window = tk.Toplevel()

    style_image_label = tk.Label(window, anchor = "nw", text = "Style image:\n Specify the url of the painting style\n image you want\n to replicate")
    content_image_label = tk.Label(window, anchor = "nw", text = "Content image:\n Specify the url of the image you want\n to modify")
    output_image_label = tk.Label(window, anchor = "nw", text = "Output image:\n Specify the name of the file\n to store the output image")
    image_size_label = tk.Label(window, anchor = "nw", text = "Image size:\n Recommended sizes: 256, 512, 1024MB")
    num_iterations_label = tk.Label(window, anchor = "nw", text = "Number iterations:\n Recommended between 50 and 500.\n The higher the number, the higher\n the quality. However, higher iterations\n will take longer to generate")

    style_image_label.pack()
    content_image_label.pack()
    output_image_label.pack()
    image_size_label.pack()
    num_iterations_label.pack()

b = tk.Button(top, height = "2", text = "Help, I'm drowning!", command = helpWindow)
b.pack()

# Labels and text fields main window
style_image_label = tk.Label(top, text = "Style image", bg = "#00BCF0", width = "31", height = "2", borderwidth = "10")
si_text_field = tk.Entry(top, width = "30", bg = "#C1E4E9", borderwidth = "16")
content_image_label = tk.Label(top, text = "Content image", bg = "#00BCF0", width = "31", height = "2", borderwidth = "10")
ci_text_field = tk.Entry(top, width = "30", bg = "#C1E4E9", borderwidth = "16")
output_image_label = tk.Label(top, text = "Output image", bg = "#00BCF0", width = "31", height = "2", borderwidth = "10")
oi_text_field = tk.Entry(top, width = "30", bg = "#C1E4E9", borderwidth = "16")
image_size_label = tk.Label(top, text = "Image size", bg = "#00BCF0", width = "31", height = "2", borderwidth = "10")
ims_text_field = tk.Entry(top, width = "30", bg = "#C1E4E9", borderwidth = "16")
num_iterations_label = tk.Label(top, text = "Number iterations", bg = "#00BCF0", width = "31", height = "2", borderwidth = "10")
ni_text_field = tk.Entry(top, width = "30", bg = "#C1E4E9", borderwidth = "16")

# Generating all the fields
style_image_label.pack()
si_text_field.pack()
content_image_label.pack()
ci_text_field.pack()
output_image_label.pack()
oi_text_field.pack()
image_size_label.pack()
ims_text_field.pack()
num_iterations_label.pack()
ni_text_field.pack()

# Called to check if user entered parameters are integers when they need to be
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Called when enter button is pushed
def callback():
    # Store user-entered values from GUI to variables
    si = si_text_field.get()
    if si == "":
        raise Exception("Please provide a style image")
    ci = ci_text_field.get()
    if ci == "":
        raise Exception("Please provide a content image")
    oi = oi_text_field.get()
    if oi == "":
        oi = "output.jpg"
    ims = ims_text_field.get()
    if ims != "" and is_number(ims) == False:
        raise Exception("Image size should be an integer. Try 256!")
    if ims == "":
        ims = "256"
    ni = ni_text_field.get()
    if ni != "" and is_number(ni) == False:
        raise Exception("Number of iterations should be an integer! Try 50!")
    if ni =="":
        ni = "50"

    # Saves images passed by user locally
    urllib.urlretrieve(si, "style-image.jpg")
    urllib.urlretrieve(ci, "content-image.jpg")

    '''
    Bash command to run neural style that uses user input to influence parameters while optimizing for docker
    Neural-style options used:
    -gpu -1 // use CPU
    -print_iter 1        // print to output for every iteration
    -init image          // initializes output image with the content image as base
    -save_iter 10        // saves image every 10 iterations
    -style_image         // image file to use for style
    -content_image       // image file to use for content
    -output_image        // file to store output image
    -image_size          // maximum side length (in pixels) of output image 
    -num_iteration       // number of iterations
    '''
    jsonStr = '{"script": "#!/bin/bash \\n th neural_style.lua -gpu -1 -print_iter 1 -init image -save_iter \'%SAVE%\' -style_image style-image.jpg -content_image content-image.jpg -output_image \'%OI%\' -image_size \'%IMS%\' -num_iterations \'%NI%\' \\n"}'.replace('%SAVE%', str((int(ni)/10))).replace('%OI%', oi).replace('%IMS%', ims).replace('%NI%', ni)
    j = json.loads(jsonStr)

    # For user to know command is being run b/c neural-style takes time to run
    print "start"
    subprocess.call(j['script'], shell=True)
    print "end"

    # Opens output image in image viewer
    jsonStr2 = '{"script": "#!/bin/bash \\n eog \'%OI%\'"}'.replace('%OI%', oi)
    j2 = json.loads(jsonStr2)
    subprocess.call(j2['script'], shell=True)

# Enter button that initiates callback
enter = tk.Button(top, text="Enter", width=10, command=callback)
enter.pack()

# Quit button
def quitButton():
    top.destroy()

quit = tk.Button(top, height = "2", text = "Take me back to the shore!", command = quitButton)
quit.pack()

# Starts GUI
top.mainloop()

