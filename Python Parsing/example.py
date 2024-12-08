import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Function to extract data using BeautifulSoup with flexible configuration
def extract_data(url, name_selector, tagline_selector, phone_selector, email_selector, profile_selector):
    response = requests.get(url)
    businesses = []
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        business_elements = soup.find_all('div', class_='directory-card')  # Update this based on actual structure

        for business in business_elements:
            # Extract name
            name_tag = business.select_one(name_selector)
            name = name_tag.text.strip() if name_tag else 'N/A'

            # Extract tagline
            tagline_tag = business.select_one(tagline_selector)
            tagline = tagline_tag.text.strip() if tagline_tag else 'N/A'

            # Extract phone number
            phone_tag = business.select_one(phone_selector)
            phone = phone_tag.text.strip() if phone_tag else 'N/A'

            # Extract profile link
            profile_link = business.select_one(profile_selector)
            profile_link = profile_link['href'] if profile_link else 'N/A'

            # Extract email
            email = 'N/A'
            email_tag = business.select_one(email_selector)
            if email_tag:
                email = email_tag['href'].replace('mailto:', '') if 'mailto:' in email_tag['href'] else 'N/A'
            
            # Fallback for emails not in mailto:
            if email == 'N/A' and business.text:
                match = re.search(email_pattern, business.text)
                if match:
                    email = match.group(0)

            businesses.append({
                'Name': name,
                'Tagline': tagline,
                'Phone': phone,
                'Profile Link': profile_link,
                'Email': email
            })
    else:
        print(f"Failed to fetch the URL with status code {response.status_code}")

    return businesses

# Main Execution
if __name__ == "__main__":
    url = "https://www.weallgrowlatina.com/directory/"

    # CSS Selectors based on website structure
    name_selector = '.directory-card__title'  # Update this based on your inspection of the website
    tagline_selector = '.directory-card__subtitle'  # Update accordingly
    phone_selector = 'a.directory-card__phone'  # Update accordingly
    email_selector = 'a[href^="mailto:"]'  # Adjust if needed
    profile_selector = 'a.directory-card__title'  # Adjust accordingly

    # Extract the data using the above selectors
    print("Extracting data using BeautifulSoup...")
    bs_data = extract_data(url, name_selector, tagline_selector, phone_selector, email_selector, profile_selector)

    # Convert the extracted data into a DataFrame
    new_data = pd.DataFrame(bs_data)

    # Output file name
    output_file = "businesses.csv"

    if not new_data.empty:
        # Check if the file exists
        if os.path.exists(output_file):
            # Read the existing data
            existing_data = pd.read_csv(output_file)

            # Combine new and existing data
            combined_data = pd.concat([existing_data, new_data])

            # Remove duplicates based on 'Name', 'Phone', and 'Email' columns
            combined_data = combined_data.drop_duplicates(subset=['Name', 'Phone', 'Email'], keep='first')

            # Save the deduplicated data back to CSV
            combined_data.to_csv(output_file, index=False)
        else:
            # If the file doesn't exist, save the new data directly to a CSV
            new_data.to_csv(output_file, index=False)

        print(f"Data successfully saved to {output_file}!")
    else:
        print("No business data found.")
