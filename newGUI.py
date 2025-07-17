

from tkinter import *
from tkinter.font import Font
import customtkinter
from PIL import Image, ImageTk
from tkinter import messagebox 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

electricity = []
water = []
groceries = []
num_months = 0

def newWindow():
    window.withdraw()
    new_window = Toplevel(window)
    new_window.geometry("920x580")
    new_window.title("Dorm Bills Forecast")
    new_window.resizable(False, False)
    new_window.config(bg='#aad6fa')

    # Create a frame for the widgets that will be scrollable
    frame = Frame(new_window)
    frame.config(bg="#aad6fa")
    frame.pack(fill="both", expand=True)

    
    label_1 = customtkinter.CTkLabel(
        master=new_window,
        text="No. of Months to Forecast:",
        text_color="black",
        font=("Calibri", 30, "bold"),
        fg_color="transparent",  
    )
    label_1.place(x=50, y=35)

    forcastMonths = customtkinter.CTkEntry(
        master=new_window,
        placeholder_text="Enter number of months to forecast...",
        font=("Arial", 16),
        width=300,
        height=40,
        border_width=2,
        corner_radius=10,
    )
    forcastMonths.place(x=55, y=75)
    numForecastMonths = forcastMonths

     # Scrollable container (Canvas and Scrollbar) below the Rent label and input field
    canvas = Canvas(new_window, bg="#FCE6A9", height=430)  
    canvas.place(x=0, y=150, relwidth=1) 

    scrollbar = Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollbar.place(x=900, y=150, relheight=1) 

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = Frame(canvas, bg="#FCE6A9")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    for col in range(5):  # Adjust column count to add space for images
        scrollable_frame.grid_columnconfigure(col, weight=1)

    def resize_frame(event):
        canvas.itemconfig(window, width=event.width)

    canvas.bind("<Configure>", resize_frame)
    
    elecLabel = customtkinter.CTkLabel(
        master=scrollable_frame,
        text="Electricity Bills",
        text_color="black",
        font=("Calibri", 25, "bold"),
        fg_color="transparent",  # Transparent background
    )
    elecLabel.grid(row=0, column=1, padx=45, pady=10, sticky="w")
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    waterLabel = customtkinter.CTkLabel(
        master=scrollable_frame,
        text="Water Bills",
        text_color="black",
        font=("Calibri", 25, "bold"),
        fg_color="transparent",  # Transparent background
    )
    waterLabel.grid(row=0, column=2, padx=65, pady=10, sticky="w")
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    groceryLabel = customtkinter.CTkLabel(
        master=scrollable_frame,
        text="Grocery Bills",
        text_color="black",
        font=("Calibri", 25, "bold"),
        fg_color="transparent",  # Transparent background
    )
    groceryLabel.grid(row=0, column=3, padx=55, pady=10, sticky="w")
    
    
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
   
    scrollable_frame
    
    def delete_month():
        global num_months
        if num_months > 0 and len(electricity) > 0:
            row_index = len(electricity) - 1

            try:
                # Destroy the month label in the same row
                month_label = scrollable_frame.grid_slaves(row=num_months, column=0)[0]
                month_label.destroy()

                # Destroy and remove other widgets
                electricity[row_index].destroy()
                water[row_index].destroy()
                groceries[row_index].destroy()

                # Remove from lists
                electricity.pop(row_index)
                water.pop(row_index)
                groceries.pop(row_index)

                # Decrement num_months
                num_months -= 1

                # Reposition remaining widgets if any exist
                for i in range(row_index):
                    # Reposition month labels
                    month_labels = scrollable_frame.grid_slaves(column=0)
                    if i < len(month_labels):
                        month_labels[len(month_labels)-1-i].grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
                    
                    # Reposition other entries
                    electricity[i].grid(row=i+1, column=1, padx=10, pady=10, sticky="w")
                    water[i].grid(row=i+1, column=2, padx=30, pady=10, sticky="w")
                    groceries[i].grid(row=i+1, column=3, padx=30, pady=10, sticky="w")

                # Update scroll region
                scrollable_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            
            except IndexError:
                show_Error(errorPrompt_tk, "No more months to delete")
            except Exception as e:
                show_Error(errorPrompt_tk,"Error deleting month")
        else:
            show_Error(errorPrompt_tk,"No months to delete")


    def add_month():
        global num_months
        num_months += 1  # Increment the label counter
        row_index = num_months

        monthnum = customtkinter.CTkLabel(
            master=scrollable_frame,
            text=f"Month {row_index}",
            text_color="black",
            font=("Calibri", 20, "bold"),
            fg_color="#FCE6A9",
        )
        monthnum.grid(row=num_months, column=0, padx=10, pady=10, sticky="w")

        elec_input = customtkinter.CTkEntry(
            master=scrollable_frame,
            placeholder_text="Enter electricity bill...",
            font=("Arial", 16),
            width=200,
            height=40,
            border_width=2,
            corner_radius=10,
        )
        elec_input.grid(row=num_months, column=1, padx=10, pady=10, sticky="w")
        electricity.append(elec_input)

        water_input = customtkinter.CTkEntry(
            master=scrollable_frame,
            placeholder_text="Enter water bill...",
            font=("Arial", 16),
            width=200,
            height=40,
            border_width=2,
            corner_radius=10,
        )
        water_input.grid(row=num_months, column=2, padx=30, pady=10, sticky="w")
        water.append(water_input)

        grocery_input = customtkinter.CTkEntry(
            master=scrollable_frame,
            placeholder_text="Enter grocery bill...",
            font=("Arial", 16),
            width=200,
            height=40,
            border_width=2,
            corner_radius=10,
        )
        grocery_input.grid(row=num_months, column=3, padx=30, pady=10, sticky="w")
        groceries.append(grocery_input)

    addButt = Image.open("ADD_BUTT.png")  
    addButt = addButt.resize((24, 24))  
    addButt_TK = ImageTk.PhotoImage(addButt)  

    prediksi = Image.open("prediksi.png")  
    prediksi = prediksi.resize((28, 28))  
    prediksi_tk = ImageTk.PhotoImage(prediksi) 

    add_month_button = customtkinter.CTkButton(
        master=new_window,  # Change the master to `new_window`
        text="Add Month",
        command=add_month,
        image=addButt_TK,
        compound="right",
        font=("Calibri", 25, "bold"),
        fg_color=('#FCE6A9'),
        text_color=("black"),
        hover_color=('#F5DCE0'),
        border_width=2,
        width=5,
        height = 50
    )
    add_month_button.place(x=515, y=20) 

    delBUTT = Image.open("deleteSKI.png")  
    delBUTT = delBUTT.resize((24, 24))  
    deleteSKI = ImageTk.PhotoImage(delBUTT)  


    delete_month_button = customtkinter.CTkButton(
        master=new_window,  # Change the master to `new_window`
        text="Delete Month",
        command=delete_month,
        image=deleteSKI,
        compound="right",
        font=("Calibri", 25, "bold"),
        fg_color=('#FCE6A9'),
        text_color=("black"),
        hover_color=('#F5DCE0'),
        border_width=2,
        width=5,
        height = 50
    )
    delete_month_button.place(x=690, y=20)

    def forecast():
        import numpy as np
        global electricity, water, groceries
            
        # When the forecast button is pressed
        if not validate_inputs():
            return

        # Get the number of months to forecast from the entry field
        try:
            numForecastMonths = int(forcastMonths.get().strip())
            if numForecastMonths <= 0:
                raise ValueError
        except ValueError:
            show_Error(errorPrompt_tk, "Please enter a valid positive integer for the number of months to forecast.")
            return

        # Extract user inputs
        electricity_data = [float(elec.get()) for elec in electricity]
        water_data = [float(water.get()) for water in water]
        grocery_data = [float(groceries.get()) for groceries in groceries]

        def select_closest_points(data):
            # If less than 4 points, use all available
            if len(data) <= 4:
                return data
            
            # Select the 4 most recent/closest points
            return data[-4:]

        def lagrange(x, y, x_target):
            # Ensure x and y have the same length
            if len(x) != len(y):
                raise ValueError("x and y must have the same length")
            
            total = 0
            for i in range(len(x)):
                # Calculate the Lagrange basis polynomial
                term = y[i]
                for j in range(len(x)):
                    if i != j:
                        term *= (x_target - x[j]) / (x[i] - x[j])
                total += term
            return total

        # Select only the 4 most recent points from the original data
        original_electricity_data = select_closest_points(electricity_data)
        original_water_data = select_closest_points(water_data)
        original_grocery_data = select_closest_points(grocery_data)

        # Generate months for the selected 4 points (1-based indexing)
        months = list(range(1, len(original_electricity_data) + 1))

        # Forecasted data storage
        forecasted_electricity = []
        forecasted_water = []
        forecasted_grocery = []

        # Forecasting loop
        for _ in range(numForecastMonths):
            # Calculate the next month index
            next_month = len(months) + 1

            # Use only the original 4 closest points for each category
            current_elec_data = select_closest_points(original_electricity_data)
            current_water_data = select_closest_points(original_water_data)
            current_grocery_data = select_closest_points(original_grocery_data)

            current_months = list(range(1, len(current_elec_data) + 1))

            # Forecast the next month's values
            next_electricity = lagrange(current_months, current_elec_data, next_month)
            next_water = lagrange(current_months, current_water_data, next_month)
            next_grocery = lagrange(current_months, current_grocery_data, next_month)

            # Append the forecasted values
            forecasted_electricity.append(next_electricity)
            forecasted_water.append(next_water)
            forecasted_grocery.append(next_grocery)
            months.append(next_month)
            # Do not update original data points with forecasted values.
            # The next forecast will only use the same 4 closest points.

        # Combine original data with forecasted data
        display_data_electricity = electricity_data + forecasted_electricity
        display_data_water = water_data + forecasted_water
        display_data_grocery = grocery_data + forecasted_grocery

        # Display the forecast window
        display_forecast_window(display_data_electricity, display_data_water, display_data_grocery, len(electricity_data))

    # Function to display the graph in a new window
    def display_forecast_window(electricity_data, water_data, grocery_data, num_months):
        # Create a new window
        forecast_window = Toplevel()
        forecast_window.title("Bills Forecast")
        forecast_window.geometry("800x600") 

        # Create the figure for plotting
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#F5DCE0')
        ax.set_facecolor('white')

        # Generate months array for plotting
        months = list(range(1, len(electricity_data) + 1))

        # Plot the data
        ax.plot(months, electricity_data, marker='o', label="Electricity Bills", color='orange')
        ax.plot(months, water_data, marker='o', label="Water Bills", color='blue')
        ax.plot(months, grocery_data, marker='o', label="Grocery Bills", color='green')

        # Add annotations for data points
        for i, (month, value) in enumerate(zip(months, electricity_data)):
            ax.annotate(f'{value:.2f}', (month, value), textcoords="offset points", xytext=(5, 5), ha='center', fontsize=8, color='orange')

        for i, (month, value) in enumerate(zip(months, water_data)):
            ax.annotate(f'{value:.2f}', (month, value), textcoords="offset points", xytext=(5, 5), ha='center', fontsize=8, color='blue')

        for i, (month, value) in enumerate(zip(months, grocery_data)):
            ax.annotate(f'{value:.2f}', (month, value), textcoords="offset points", xytext=(5, 5), ha='center', fontsize=8, color='green')
        # Highlight extrapolated values
        ax.axvline(x=num_months, color='red', linestyle='--', label="Start of Extrapolation ")

        # Add titles and labels
        ax.set_title("Bills Forecast", fontsize=16)
        ax.set_xlabel("Month Number", fontsize=14)
        ax.set_ylabel("Bill Amount", fontsize=14)
        ax.legend(fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=forecast_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Add a close button
        close_button = Button(forecast_window, text="Close", command=forecast_window.destroy)
        close_button.pack(pady=10)

    def validate_inputs():
        # Validate rent input
        forcastMonths_text = forcastMonths.get().strip()  # Correctly access the entry's value
        if not forcastMonths_text.isdigit():  # Check if it is a positive integer
            show_Error(errorPrompt_tk, "Please enter a valid numeric value for the number of months to forecast.")
            return False

        if len(electricity) < 2 or len(water) < 2 or len(groceries) < 2:
            show_Error(errorPrompt_tk, "Please enter data for at least two months.")
            return False
        # Check electricity inputs
        for elec_input in electricity:
            value = elec_input.get().strip()  # Get the text and remove extra spaces
            if not value.replace('.', '', 1).isdigit():  # Allow decimal numbers
                show_Error(errorPrompt_tk, "Please make sure all fields are filled with valid numbers.")
                return False  # Return False if any input is invalid

        for water_input in water:
            value = water_input.get().strip() 
            if not value.replace('.', '', 1).isdigit():  
                show_Error(errorPrompt_tk,"Error", "Please make sure all fields are filled with valid numbers.")
                return False  

        for grocery_input in groceries:
            value = grocery_input.get().strip()  
            if not value.replace('.', '', 1).isdigit():  
                show_Error(errorPrompt_tk, "Please make sure all fields are filled with valid numbers.")
                return False  
        return True  

    foreCast = customtkinter.CTkButton(
        master=new_window,  # Change the master to `new_window`
        text="Forecast",
        command=forecast,
        image=prediksi_tk,
        compound="right",
        font=("Calibri", 25, "bold"),
        fg_color=('#FCE6A9'),
        text_color=("black"),
        hover_color=('#F5DCE0'),
        border_width=2,
        width=375,
        height = 50
    )
    foreCast.place(x=515, y=80)
    
    errorPrompt = Image.open("errorPrompt.png")  
    errorPrompt = errorPrompt.resize((100, 200))  
    errorPrompt_tk = ImageTk.PhotoImage(errorPrompt)  

    def show_Error(errorPrompt_tk, error_message):
        # Create a custom Toplevel error dialog
        error_window = Toplevel()
        error_window.title("Error")
        error_window.geometry("300x200") 
        error_window.resizable(False, False)  
        
        # Display the image
        img_label = Label(error_window, image=errorPrompt_tk)
        img_label.image = errorPrompt_tk 
        img_label.place(y=40, x=220)

        # Display the error message with wrapping
        error_label = customtkinter.CTkLabel(
            error_window,
            text=error_message,
            fg_color="#FFCCCC",  # Light red background color
            text_color="black",
            corner_radius=10,  # Rounded edges
            font=("Arial", 13, "bold"),
            width=280,
            height=40,  # Adjust height for multiline text
            wraplength=260  # Wrap text within 260 pixels
        )
        error_label.pack(pady=5)

        # Add a dismiss button
        dismiss_button = customtkinter.CTkButton(
            master=error_window,
            text="Dismiss",
            command=error_window.destroy,
            font=("Calibri", 14, "bold"),
            fg_color=('#FCE6A9'),
            text_color="black",
            hover_color=('#F5DCE0'),
            border_width=2,
            width=80,  # Adjusted button width
            height=30  # Adjusted button height
        )
        dismiss_button.place(x=110, y=140)  # Centered the button horizontally

        error_window.mainloop()

        # Example usage
        root = Tk()
        root.withdraw()  # Hide the main window

        # Call the custom error dialog
        show_Error(errorPrompt_tk, "Please enter valid data for the required fields. The input must not be empty or invalid.")

        root.mainloop()



#main window
window = Tk()
window.geometry("920x580")
window.title("Dorm Bills Forecast")
window.resizable(False, False)

label = customtkinter.CTkLabel(
    master=window,
    text="Dorm Bills Forecast",
    text_color="black", 
    fg_color = "#aad6fa",
    font=("Calibri", 50, "bold"),
    corner_radius=10,  # Rounded corners
    width=10,
    
)
label.pack(pady=0)
label.place(x=270,y=200)


def click():
    newWindow()

predictIcon = Image.open("predict.png")  
predictIcon = predictIcon.resize((24, 24))  
predictIcon_tk = ImageTk.PhotoImage(predictIcon)  # Convert to Tkinter-compatible format

backgroundImg = Image.open("stonks.png")  
backgroundImg = backgroundImg.resize((920, 580))  
backgroundImg_tk = ImageTk.PhotoImage(backgroundImg)  

background_label = Label(window, image=backgroundImg_tk)
background_label.place(relwidth=1, relheight=1)
background_label.lower()

button = customtkinter.CTkButton(
    master=window, 
    text="BEGIN", 
    image = predictIcon_tk,
    command=click,
        compound="right",
        font=("Calibri", 25, "bold"),
        fg_color=('#FCE6A9'),
        text_color=("black"),
        hover_color=('#F5DCE0'),
        border_width=2,
        width=5,
        height = 50
    )
button.place(relx=0.5, rely=0.52, anchor=customtkinter.CENTER)

window.config(background='#AAD6FA')
window.mainloop()




