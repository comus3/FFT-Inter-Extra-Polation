from function_library import function
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft


def addZeros(data,coef):
    res = np.zeros(len(data)*(coef))
    for i in range(len(data)):
        res[coef*i]=data[i]
    return res
def generate_function_values(func, start, stop, step):
    """
    Generate an array of function values over a specified range with a given step size.

    Parameters:
    - func: The function for which values need to be generated.
    - start: The starting value of the range.
    - stop: The ending value of the range (exclusive).
    - step: The step size between values in the range.

    Returns:
    - An array containing the function values at each point in the specified range.
    """
    if step <= 0:
        raise ValueError("Step size must be positive")

    # Create an array of values from start to stop with the specified step size
    x = np.arange(start, stop, step)

    # Apply the function to each element in the array and store the results in a new array
    y = np.array([func(x_val) for x_val in x])

    return y


def compute_fft(input_array):
    """
    Compute the Fast Fourier Transform (FFT) of a given NumPy array.

    Parameters:
    - input_array: The input array for which the FFT needs to be computed.

    Returns:
    - The FFT of the input array.
    """
    # Compute the FFT using numpy.fft.fft
    fft_result = np.fft.fft(input_array)

    return fft_result

def generate_ifft_points(fft_data, start, stop, step):
    """
    Generate points of the Inverse Fast Fourier Transform (iFFT) from an FFT result.

    Parameters:
    - fft_data: The input FFT data for which iFFT points need to be generated.
    - start: The starting value of the range.
    - stop: The ending value of the range (exclusive).
    - step: The step size between points in the range.

    Returns:
    - An array containing the iFFT points at each point in the specified range.
    """
    if step <= 0:
        raise ValueError("Step size must be positive")

    # Determine the number of points to generate based on the range and step size
    num_points = int((stop - start) / step)

    # Generate an array of frequencies corresponding to the iFFT points
    frequencies = np.fft.fftfreq(len(fft_data), d=step)

    # Compute the iFFT
    ifft_result = np.fft.ifft(fft_data)

    # Select the first 'num_points' values from the iFFT result
    ifft_points = ifft_result[:num_points]

    return ifft_points

def plot_points(x, y, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Plot an array of points.

    Parameters:
    - x: The x-coordinates of the points.
    - y: The y-coordinates of the points.
    - title: The title of the plot (optional).
    - xlabel: The label for the x-axis (optional).
    - ylabel: The label for the y-axis (optional).
    """
    plt.figure()
    plt.scatter(x, y, label="Points")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk

    def create_function_reference(function_name):
        functionLibrary = globals()
        
        if function_name in functionLibrary:
            new_function = functionLibrary[function_name]
            return new_function
        else:
            raise ValueError(f"Function '{function_name}' does not exist.")

    def generate_and_plot():
        # Retrieve values from input fields and perform the generation and plotting
        selected_option = option_var.get()
        start_in = float(start_in_entry.get())
        end_in = float(end_in_entry.get())
        step_in = float(step_in_entry.get())
        start_out = float(start_out_entry.get())
        end_out = float(end_out_entry.get())
        step_out = float(step_out_entry.get())

        print("Selected Option:", selected_option)
        print("Start In:", start_in)
        print("End In:", end_in)
        print("Step In:", step_in)
        print("Start Out:", start_out)
        print("End Out:", end_out)
        print("Step Out:", step_out)
        
        #signalFunc = create_function_reference("function."+selected_option)
        signalFunc =function.func5
        x_Values_IN = np.arange(start_in, end_in, step_in)
        dataPRE = generate_function_values(signalFunc,start_in,end_in,step_in)
        modified_Data = addZeros(dataPRE,int(step_in/step_out))
        num_Of_Out_Points = len(modified_Data)
        x_Values_OUT = np.linspace(start_out,end_out,num_Of_Out_Points)
        dataPOST = generate_ifft_points(compute_fft(modified_Data),start_out,end_out,step_out)
        plot_points(x_Values_IN,dataPRE,"Donnees avant")
        plot_points(x_Values_OUT,dataPOST,"Donnees apres")


    app = tk.Tk()
    app.title("Function Generator")

    # Scrolling menu
    option_label = tk.Label(app, text="Select Function:")
    option_label.pack()
    options = ["triangle", "sineSum", "sine", "func1", "func2", "func3", "func4", "func5", "blaster"]
    option_var = tk.StringVar(app)
    option_menu = ttk.Combobox(app, textvariable=option_var, values=options)
    option_menu.pack()

    # Input fields
    input_frame = tk.Frame(app)
    input_frame.pack()

    start_in_label = tk.Label(input_frame, text="Start In:")
    start_in_label.grid(row=0, column=0)
    start_in_entry = tk.Entry(input_frame)
    start_in_entry.grid(row=0, column=1)

    end_in_label = tk.Label(input_frame, text="End In:")
    end_in_label.grid(row=1, column=0)
    end_in_entry = tk.Entry(input_frame)
    end_in_entry.grid(row=1, column=1)

    step_in_label = tk.Label(input_frame, text="Step In:")
    step_in_label.grid(row=2, column=0)
    step_in_entry = tk.Entry(input_frame)
    step_in_entry.grid(row=2, column=1)

    start_out_label = tk.Label(input_frame, text="Start Out:")
    start_out_label.grid(row=0, column=2)
    start_out_entry = tk.Entry(input_frame)
    start_out_entry.grid(row=0, column=3)

    end_out_label = tk.Label(input_frame, text="End Out:")
    end_out_label.grid(row=1, column=2)
    end_out_entry = tk.Entry(input_frame)
    end_out_entry.grid(row=1, column=3)

    step_out_label = tk.Label(input_frame, text="Step Out:")
    step_out_label.grid(row=2, column=2)
    step_out_entry = tk.Entry(input_frame)
    step_out_entry.grid(row=2, column=3)

    # Generate and plot button
    generate_button = tk.Button(app, text="Generate and Plot", command=generate_and_plot)
    generate_button.pack()

    app.mainloop()
