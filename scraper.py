from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_linkedin_jobs(url):
    driver = init_driver()
    driver.get(url)
    jobs = []

    try:
        for i in range(5):  # Scroll and load more jobs
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")

            for job_card in job_cards:
                ActionChains(driver).move_to_element(job_card).click().perform()
                time.sleep(1)  # Wait for job details to load

                # Extract job details
                try:
                    title = driver.find_element(By.CSS_SELECTOR, ".topcard__title").text
                    company = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link").text
                    location = driver.find_element(By.CSS_SELECTOR, ".topcard__flavor--bullet").text
                    applicants = driver.find_element(By.CSS_SELECTOR, "figcaption.num-applicants__caption").text  # Example: "Be among the first 25 applicants"
                    time_posted = driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'posted-time-ago__text')]").text
                    # seniority_level = driver.find_element(By.XPATH,
                    #                                       "//span[text()='Seniority level']/following-sibling::span").text
                    # employment_type = driver.find_element(By.XPATH,
                    #                                       "//span[text()='Employment type']/following-sibling::span").text
                    # job_function = driver.find_element(By.XPATH,
                    #                                    "//span[text()='Job function']/following-sibling::span").text
                    # industries = driver.find_element(By.XPATH,
                    #                                  "//span[text()='Industries']/following-sibling::span").text

                    # description = driver.find_element(By.XPATH, "//div[contains(@class, 'show-more-less-html__markup relative overflow-hidden show-more-less-html__markup--clamp-after-5')]").text

                    description = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup").text
                    # seniority_level = driver.find_element(By.XPATH,
                    #                                       "//h3[text()='Seniority level']/following-sibling::span").text
                    # employment_type = driver.find_element(By.XPATH,
                    #                                       "//h3[text()='Employment type']/following-sibling::span").text
                    # job_function = driver.find_element(By.XPATH,
                    #                                    "//h3[text()='Job function']/following-sibling::span").text
                    # industries = driver.find_element(By.XPATH,
                    #                                  "//h3[text()='Industries']/following-sibling::span").text

                    # Extract Seniority Level
                    # seniority_level = driver.find_element(By.XPATH, "//ul/li[h3[text()='Seniority level']]/span").text
                    # # Extract Employment Type
                    # employment_type = driver.find_element(By.XPATH,
                    #                                       "//h3[text()='Employment type']/following-sibling::span").text
                    #
                    # # Extract Job Function
                    # job_function = driver.find_element(By.XPATH,
                    #                                    "//h3[text()='Job function']/following-sibling::span").text
                    #
                    # # Extract Industries
                    # industries = driver.find_element(By.XPATH, "//h3[text()='Industries']/following-sibling::span").text
                    seniority_level = driver.find_element(By.XPATH,
                                                          "//li[h3[contains(text(), 'Seniority level')]]/span").text
                    employment_type = driver.find_element(By.XPATH, "//li[h3[contains(text(), 'Employment type')]]/span").text
                    job_function = driver.find_element(By.XPATH, "//li[h3[contains(text(), 'Job function')]]/span").text
                    industries = driver.find_element(By.XPATH, "//li[h3[contains(text(), 'Industries')]]/span").text

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "applicants": applicants,
                        "time_posted": time_posted,
                        "seniority_level": seniority_level,
                        "employment_type": employment_type,
                        "job_function": job_function,
                        "industries": industries,
                        "description": description,
                    })
                    print(jobs[-1])
                except Exception as e:
                    print(f"Error extracting job details: {e}")

                time.sleep(2)

            # Scroll down to load more jobs
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(10)  # Wait for more jobs to load

    except KeyboardInterrupt:
        print("Scraping stopped.")
    finally:
        driver.quit()
        return jobs


def get_html(url):
    try:
        # Set headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Send a GET request with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        html_content = None

    if html_content:
        print("HTML content fetched successfully.")
        # Save the HTML to a file
        with open("website.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print("HTML content saved to 'website.html'.")

# Usage
if __name__ == "__main__":
    # get_html("https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0&currentJobId=4119711273")

    linkedin_jobs_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States"
    jobs_data = scrape_linkedin_jobs(linkedin_jobs_url)
    print(f"Scraped {len(jobs_data)} jobs.")
    for job in jobs_data[:5]:  # Print the first 5 jobs
        print(job)