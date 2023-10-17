
# Part of the desing for this programe was generated using Tkinter Designer by Parth Jadhav. Credits on the next line
# https://github.com/ParthJadhav/Tkinter-Designer
# Please make sure that you have all the necesary libraries for the import and adjust your path file to your local ubication.

from pathlib import Path
import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from MCForecastTools import MCSimulation

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\marco\OneDrive\Desktop\Project-1\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk(className='Comodity comparer')

window.geometry("1000x796")
window.configure(bg = "#130660")

# Global Variables ----------------------------------------------------

drop_list = ['Stock','Stock Splits','Splits','Dividends','Volume','Low','High','Open','Capital Gains']
portfolio = {}
sim_portfolio = pd.DataFrame()
portfolio_list = []
v = StringVar(window, "1")
weight_list = []

    
# Global functions ----------------------------------------------------

def puller(ticker, time):
            info = yf.Ticker(ticker)
            history = info.history(period=time)
            for column in drop_list:
                if column in history.columns:
                    history.drop(columns=[column],inplace=True)
            history = history.reset_index()
            if 'Date' in history.columns and history.shape[0] > 0:
                history['Date'] = history['Date'].dt.strftime('%Y-%m-%d')
                history = history.set_index('Date')
            history.rename(columns={'Close': ticker}, inplace=True)
            
            return history

def UI_puller():
            asset_name = asset_name_box.get()
            asset_name = asset_name.upper()
            asset_time = asset_time_box.get()
            result = puller(asset_name,asset_time)
            if result.empty:
                top= Toplevel(window)
                top.geometry("250x100")
                top.title("Error 404")
                Label(top, text= "ERROR: TICKER NOT FOUND", font=('Arial 10 bold')).place(x=40,y=30)
            else:
                portfolio[asset_name] = result
                portfolio_list.append(asset_name)
                yposrad = 210
                xposrad = 90
                xposcheck = 740
                yposcheck = 210
                xpostype = 820
                ypostype = 223
                switch = False
                for (text, value) in portfolio.items():
                    radio_button = Radiobutton(window, text = text,background='#AF90F2', value = text, variable = v, font=('Arial 10 bold'), command=performance_display)
                    radio_button.place(x=xposrad, y=yposrad)
                    if switch == True:
                         yposrad = yposrad + 20
                         xposrad = 90
                         switch = False
                    elif switch == False:
                         xposrad = 190
                         switch = True
                for (text, value) in portfolio.items():
                    check_button = tk.Checkbutton(window, text=text,variable=text, onvalue=1, offvalue=0,background='#AF90F2', command=print(value))
                    check_button.place(x=xposcheck, y=yposcheck)
                    weight_box = tk.Entry(window, background='#CD86D3', width=20)
                    canvas.create_window(xpostype , ypostype, window = weight_box, width=30)
                    if switch == True:
                        yposcheck = yposcheck + 20
                        ypostype = ypostype + 20
                        xpostype = 820
                        xposcheck = 740
                        switch = False
                    elif switch == False:
                        xposcheck = 850
                        xpostype = 920
                        switch = True
                    
def merge_dfs():
    dfs = list(portfolio.values())
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = merged_df.join(df)
    df_list = []
    for column in merged_df:
        df_list.append(pd.DataFrame(merged_df[column]))
    combined = pd.concat(df_list,axis=1,keys=merged_df.columns)
    renamed_columns = {ticker: 'close' for ticker in merged_df.columns}
    combined.rename(columns=renamed_columns, level=1, inplace=True)
    return combined

def performance_display():
    ticket = str(v.get())
    volatility = 0.0
    cumu_percent = 0.0
    performance_graph = Figure(figsize=(3,3), facecolor="#AF90F2")
    ax_1 = performance_graph.add_subplot()
    ax_1.set_facecolor("#AF90F2")
    ax_1.fill_between(x=portfolio[ticket].index, y1=portfolio[ticket][ticket],alpha=0.7)
    ax_1.tick_params(labelsize=7, colors='white')
    performance_graph.autofmt_xdate()
    ax_1.plot(portfolio[ticket].index, np.asanyarray(portfolio[ticket][ticket], int), color='deepskyblue')

    canvas2 = FigureCanvasTkAgg(figure=performance_graph, master=window)
    canvas2.draw()
    canvas2.get_tk_widget().place(x=345, y=196)

    canvas.create_text(
        357,
        500,
        anchor="nw",
        text=f"Asset Volatility:\n{volatility}",
        fill="#000000",
        font=("Inter SemiBold", 15 * -1)
    )

    canvas.create_text(
        500,
        500,
        anchor="nw",
        text=f"Cumulative growth \npercentage:\n{cumu_percent}%",
        fill="#000000",
        font=("Inter SemiBold", 15 * -1)
    )

def simulation():
    df = merge_dfs()
    mc_simulation = MCSimulation(
        portfolio_data = df,
        # weights = [.50,.10,.10,.10,.10,.10],
        num_simulation = 100,
        num_trading_days = int(simulation_days.get())
    )
    # mc_cumulative = mc_simulation.calc_cumulative_return()
    return mc_simulation

def mc_simulation_window():
    mc_simulation = simulation()
    sim_graph_data = mc_simulation.calc_cumulative_return()
    tbl = mc_simulation.summarize_cumulative_return()
    initial_investment = 10000
    ci_lower = round(tbl[8]*initial_investment,2)
    ci_upper = round(tbl[9]*initial_investment,2)
    top = Toplevel(window)
    top.config(bg="#130660")
    top.geometry("850x700")
    top.title("Monte Carlo Simulation")
    sim_graph = Figure(figsize=(7,5), facecolor="#AF90F2")
    ax_1 = sim_graph.add_subplot()
    ax_1.set_facecolor("#AF90F2")
    ax_1.plot(sim_graph_data)
    ax_1.grid(visible=True)
    ax_1.tick_params(labelsize=7, colors='white')
    canvas3 = FigureCanvasTkAgg(figure=sim_graph, master=top)
    canvas3.draw()
    canvas3.get_tk_widget().place(x=70, y=70)
    Label(top, text= "Simulation result", font=('Arial 20 bold'), background="#130660",fg='white').place(x=70,y=20)
    Label(top, text= f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio\n"
                    f" over the next 30 years will end within in the range of\n"
                    f" ${ci_lower} and ${ci_upper}", font=('Arial 15 bold'), 
                    background="#130660",fg='white').place(x=70,y=600)


# UI Code --------------------------------------------------------------

canvas = Canvas(
    window,
    bg = "#130660",
    height = 796,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)


## Input boxes -----------------------------------

asset_name_box = tk.Entry(window, background='#CD86D3')
canvas.create_window(120, 702, window= asset_name_box)

asset_time_box = tk.Entry(window, background='#CD86D3')
canvas.create_window(354, 702, window= asset_time_box)

simulation_days = tk.Entry(window, background='#CD86D3')
canvas.create_window(650, 736, window= simulation_days)

## Buttons ----------------------------------------

new_asset_button = tk.Button(text='Get information', command=UI_puller, bg='brown',background='#43AC1D', fg='white', font=('helvetica', 15, 'bold'))
canvas.create_window(240.0,750.0, window=new_asset_button)

mc_simulation_button = tk.Button(text='Run Simulation', command=mc_simulation_window, bg='brown',background='#43AC1D', fg='white', font=('helvetica', 15, 'bold'))
canvas.create_window(875,710.0, window=mc_simulation_button)

# delete_asset = tk.Button(text='Delete selected asset', command=print('Placeholder'), bg='brown',background='#865CDF', fg='white', font=('helvetica', 12, 'bold'))
# canvas.create_window(170.0,545.0, window=delete_asset)


## Frames and Icons---------------------------

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("header.png"))
image_1 = canvas.create_image(
    500.0,
    41.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("money_header.png"))
image_2 = canvas.create_image(
    72.0,
    41.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    244.0,
    614.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    763.0,
    614.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    493.0,
    149.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    168.0,
    149.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    824.0,
    149.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    244.0,
    713.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    762.0,
    713.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    120.0,
    706.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    354.0,
    706.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    650.0,
    740.0,
    image=image_image_12
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    493.0,
    379.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    168.0,
    379.0,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    824.0,
    379.0,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    131.0,
    613.0,
    image=image_image_18
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    339.0,
    613.0,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    636.0,
    614.0,
    image=image_image_20
)

## Text ------------------------------

canvas.create_text(
    125.0,
    20.0,
    anchor="nw",
    text="Comodity comparer 3000",
    fill="#000000",
    font=("Inter SemiBold", 30 * -1)
)

canvas.create_text(
    163.0,
    602.0,
    anchor="nw",
    text="Add new asset",
    fill="#000000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    664.0,
    602.0,
    anchor="nw",
    text="Run a Montecarlo sim.",
    fill="#000000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    43.0,
    135.0,
    anchor="nw",
    text="Current comodities on file",
    fill="#0A0000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    720.0,
    128.0,
    anchor="nw",
    text="Select assets to run the\n  Montecarlo simulation",
    fill="#0A0000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    400.0,
    128.0,
    anchor="nw",
    text="Past performance of \n  the selected asset",
    fill="#0A0000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    29.0,
    661.0,
    anchor="nw",
    text="Exchange Ticker name",
    fill="#0A0000",
    font=("JockeyOne Regular", 18 * -1)
)

canvas.create_text(
    280.0,
    661.0,
    anchor="nw",
    text="Time period to pull",
    fill="#0A0000",
    font=("JockeyOne Regular", 18 * -1)
)

canvas.create_text(
    559.0,
    667.0,
    anchor="nw",
    text="How many trading days \n         to simulate?",
    fill="#0A0000",
    font=("JockeyOne Regular", 18 * -1)
)

#------------------------------------

window.resizable(False, False)
window.mainloop()
