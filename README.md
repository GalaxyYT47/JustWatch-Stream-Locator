# JustWatch Stream Locator

## Description
JustWatch Stream Locator is a Python script designed to help users find the streaming services available for a specific movie or TV show in various countries and continents. The script uses the JustWatch website to determine where a title is streaming globally, providing a convenient way for users to discover streaming platforms that offer their desired content.

## Features
- Global Streaming Service Identification: Determines which streaming services offer a specific title in different countries.
- Continental and Country-wise Breakdown: Organizes streaming services availability by continent and country.
- Code is easily customizable for adding or removing streaming services.
- User-friendly Interface: Simple input method for URLs and clear, organized output of results.

## How It Works
1. URL Input: The user inputs a JustWatch URL of the movie or TV show.
2. Data Extraction: The script scrapes the JustWatch page for the given URL, extracting information about available streaming services.
3. Service Availability Analysis: It analyzes which streaming services offer the title in different countries and continents.
4. Display Results: Outputs a list of streaming services along with the countries and continents where they are available for the given title.

## Usage
1. Run the script.
2. Enter the JustWatch URL of the movie or TV show when prompted.
3. View the list of streaming services and the regions where the title is available.

4. ## Requirements
- Python 3
- `requests` library
- `beautifulsoup4` library
