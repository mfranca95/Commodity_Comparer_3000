# Project-1
# Commodity Investment Analyzer
​
Commodity Comparer 300 is a game-changer, providing users with a simple and intuitive platform to compare commodity prices, access historical data, and analyze trends. 
​
## Table of Contents
​
- [Commodity_Comparer_3000](#project-name)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)
​
## About
​
The Commodity Investment Analyzer is a data-driven tool designed to assist investors in making informed decisions about investing in various commodities. Leveraging historical data and advanced analytical techniques, the tool aims to answer critical questions and provide insights into the performance of different commodities.Features and Components:

Data Collection: The tool will collect historical data for a selected list of commodities, including Physical Gold, Physical Silver, Real Estate prices (Average Sale price), SPY, Nasdaq, Bitcoin, and ETH, through APIs such as yfinance. This data will serve as the foundation for analysis.

Percentile Change Comparison: The tool will calculate and compare the percentile change in the prices of these commodities over time, allowing users to identify trends and patterns.

Monte Carlo Simulations: Monte Carlo simulations will be employed to simulate various investment scenarios. Users can input their investment amounts and timeframes, and the tool will provide probabilistic forecasts for potential growth.

Visualization: Matplotlib will be used to create informative visualizations. This will include line charts  to make complex data more accessible.

Pandas Data Analysis: Pandas will be utilized for data cleaning, manipulation, and statistical analysis to answer research questions and provide relevant insights.

API Integration: Data will be continuously updated via APIs to ensure that the tool provides real-time information for decision-making.


​
## Getting Started
​
Explain how to get your project up and running on the user's local machine.
​
### Prerequisites
​​
Python (v3.6 or higher)
​
### Installation
​
- clone the repository using the following command in your console: git clone https://github.com/mfranca95/Commodity_Comparer_3000.git
- Get into an environment that you want to run the program in.
- Install all the necessary libraries (list at the end of the section)
- Inside the comparer.py file in line 24, change the "C:\Users\marco\OneDrive\Desktop\Project-1\build\assets\frame0" to "(your location)\assets\frame0", "your location" been the address in where you saved the information of the app.
​​
Necessary dependencies:
​
​npm install 
pip install matplotlib
pip install pandas
pip install pathlib
pip install yfinance

​
## Usage
​
In the majority of cases, the end user of an application is not a person who has knowledge in the programming area. This is why developing an analysis tool with an easy-to-use interface is so crucial.
The objective of the commodity comparer is to make accessible financial analysis for people who are not versed in the programming area but have knowledge in the financial field.
The use of Yahoo Finance gives the application an always 'up-to-date' information data source, which serves as a future-proofs design.
​
## Contributing
​
If you're open to contributions from the community, explain how others can contribute to your project. Include guidelines for code formatting, issue reporting, and pull requests.
​
## Acknowledgments
​
Part of the design for this program was generated using Tkinter Designer by Parth Jadhav. Credits on the next line.
https://github.com/ParthJadhav/Tkinter-Designer












