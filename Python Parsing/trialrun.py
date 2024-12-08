import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Function to extract data using BeautifulSoup
def extract_with_beautifulsoup(url):
    response = requests.get(url)
    businesses = []
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust class name based on the provided HTML structure
        business_elements = soup.find_all('div', class_='sa-free')

        for business in business_elements:
            # Extract name
            name_tag = business.find('a', class_='sa-bus-name')
            name = name_tag.text.strip() if name_tag else 'N/A'

            # Extract tagline or description
            tagline_tag = business.find('div', class_='sa-bus-tag')
            tagline = tagline_tag.text.strip() if tagline_tag else 'N/A'

            # Extract phone number
            phone_tag = business.find('a', class_='sa-tel')
            phone = phone_tag.text.strip() if phone_tag else 'N/A'

            # Extract profile link (website)
            website_tag = business.find('a', class_='sa-btn sa-prof')
            website = website_tag['href'] if website_tag else 'N/A'

            # Placeholder for email, as no explicit email is mentioned in the HTML provided
            email = 'N/A'

            # Extract business address (no address found in the example HTML, so we set it to N/A)
            address = 'N/A'
            
            # Extract city (no city found in the provided HTML, so we set it to N/A)
            city = 'N/A'

            # Extract postcode (no postcode found in the provided HTML, so we set it to N/A)
            postcode = 'N/A'

            # Extract business tier (not found in the provided HTML, so we set it to N/A)
            tier = 'N/A'

            # NAICS info, social media links and others were not present in the provided layout, so they are omitted
            naics_info = []

            # No social media links were provided in the example HTML, so this remains empty
            social_links = []

            # Append the business information to the list
            businesses.append({
                'Name': name,
                'Tagline': tagline,
                'Phone': phone,
                'Website': website,
                'Email': email,
                'Address': address,
                'City': city,
                'Postcode': postcode,
                'Tier': tier,
                'NAICS Info': naics_info,
                'Social Media Links': social_links
            })
    else:
        print(f"Failed to fetch the URL with BeautifulSoup. Status Code: {response.status_code}")

    return businesses


# Main Execution
if __name__ == "__main__":
    url = "https://www.sbdpro.com/events-entertainment"  # New URL

    # Extract using BeautifulSoup
    print("Extracting data using BeautifulSoup...")
    bs_data = extract_with_beautifulsoup(url)

    # Convert to DataFrame
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

            # Remove duplicates
            combined_data = combined_data.drop_duplicates(subset=['Name', 'Phone', 'Email'], keep='first')

            # Save the deduplicated data
            combined_data.to_csv(output_file, index=False)
        else:
            # Save new data directly if no file exists
            new_data.to_csv(output_file, index=False)

        print(f"Data successfully saved to {output_file}!")
    else:
        print("No business data found.")
