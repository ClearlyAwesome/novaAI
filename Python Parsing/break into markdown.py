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
        business_elements = soup.find_all('div', class_='directory-card')  # Adjusted class based on provided HTML structure

        for business in business_elements:
            # Extract name
            name_tag = business.find('h4', class_='directory-card__title')
            name = name_tag.text.strip() if name_tag else 'N/A'

            # Extract tagline or description
            tagline_tag = business.find('span', class_='directory-card__subtitle')
            tagline = tagline_tag.text.strip() if tagline_tag else 'N/A'

            # Extract phone number
            phone_tag = business.find('a', href=lambda href: href and href.startswith('tel:'))
            phone = phone_tag.text.strip() if phone_tag else 'N/A'

            # Extract website link
            website_tag = business.find('a', href=lambda href: href and href.startswith('http'))
            website = website_tag['href'] if website_tag else 'N/A'

            # Extract email from mailto: links
            email = 'N/A'
            email_links = business.find_all('a', href=True)
            for link in email_links:
                if 'mailto:' in link['href']:
                    email = link['href'].replace('mailto:', '')

            # Extract business address
            address_tag = business.find('span', class_='directory-card__address')
            address = address_tag.text.strip() if address_tag else 'N/A'

            # Extract city
            city_tag = business.find('span', class_='directory-card__city')
            city = city_tag.text.strip() if city_tag else 'N/A'

            # Extract postcode
            postcode_tag = business.find('span', class_='directory-card__postcode')
            postcode = postcode_tag.text.strip() if postcode_tag else 'N/A'

            # Extract business tier (Tier 1, Tier 2)
            tier = tagline.strip() if tagline else 'N/A'

            # Extract NAICS codes and capabilities (from the dropdown details)
            naics_info = []
            naics_details = business.find_all('details', class_='directory-card__dropdown')
            for naics in naics_details:
                naics_code = naics.find('td').text.strip() if naics.find('td') else 'N/A'
                naics_description = naics.find_all('td')[1].text.strip() if len(naics.find_all('td')) > 1 else 'N/A'
                naics_capability = naics.find_all('td')[2].text.strip() if len(naics.find_all('td')) > 2 else 'N/A'
                naics_info.append({
                    'NAICS Code': naics_code,
                    'Description': naics_description,
                    'Capability': naics_capability
                })

            # Extract social media links
            social_links = []
            social_media = business.find_all('a', class_='socials__item')
            for link in social_media:
                social_links.append(link['href'])

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
    url = "https://goed.nv.gov/emerging-small-business-directory/"

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
