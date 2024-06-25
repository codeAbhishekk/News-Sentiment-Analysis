# News Sentiment Analysis Project

Welcome to the News Sentiment Analysis Project! This project involves building a machine learning model that analyzes the sentiment of news articles. It is developed using the Django framework and utilizes Beautiful Soup for web scraping.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project aims to scrape news headlines and content from the NDTV news website, analyze their sentiment using NLP techniques, and display the results on a web application. The web app consists of three pages:

- [Home Page](#home-page): Shows the scraped news and their sentiments, updated regularly.
- [Analyze News Text](#analyze-news-text): A form where users can input a sentence and get its sentiment.
- [Upload CSV](#upload-csv): Allows users to upload a CSV file containing news headlines and content, and displays their sentiments in a table.

---

## Features
- **Web Scraping**: Extracts news headlines and content from the NDTV news website using Beautiful Soup.
- **Sentiment Analysis**: Analyzes the sentiment of the news articles using `TextBlob`.
- **Dynamic Content**: The home page updates automatically as the news content on the website changes.
- **User Interaction**: Users can analyze the sentiment of their own text or upload CSV files for batch sentiment analysis.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- Beautiful Soup 4
- Requests
- Pandas
- TextBlob

---

## Installation

Clone the repository:

## Usage Guide

### Home Page

The home page displays the latest news articles scraped from NDTV along with their sentiment analysis. The page updates automatically as the news content changes on the website.

### Analyze News Text

Navigate to the "Analyze News Text" page using the link on the home page. Here, you can input any sentence and click "Analyze" to see the sentiment of the text.

### Upload CSV

Navigate to the "Upload CSV" page using the link on the home page. Upload a CSV file containing news headlines and content. After submitting, the page will display the sentiment of each news headline in a table.

---

## Screenshots

Here are some suggested screenshots to include in your README.md:

1. **Home Page**: Displaying the scraped news articles and their sentiments.
   ![Home Page](screenshots/home-page.png)

2. **Analyze News Text**: The form for inputting text and analyzing sentiment.
   ![Analyze News Text](screenshots/analyze_text.png)

3. **Upload CSV**: The interface for uploading a CSV file and displaying sentiments.
   ![Upload CSV](screenshots/analyze_csv.png)

*Replace the placeholder links with actual screenshots from your application.*

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Web Scraping**: Beautiful Soup
- **Sentiment Analysis**: TextBlob
- **Data Handling**: Pandas

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**
