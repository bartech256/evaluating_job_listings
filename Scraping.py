import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initialize the Selenium WebDriver with Chrome options."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def save_to_json(jobs, filename):
    """Save a list of jobs to a JSON file."""
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=2, ensure_ascii=False)

def extract_field(driver, field_name):
    """Extract a job criteria field based on the field name."""
    try:
        field_element = driver.find_element(
            By.XPATH, f"//li[h3[contains(., '{field_name}')]]/span"
        )
        return field_element.text.strip()  # Extract and return the text
    except Exception as e:
        print(f"Error extracting field '{field_name}': {e}")
        return "N/A"  # Default value if field is missing

def scrape_linkedin_jobs(url, num_jobs=1000, batch_size=100):
    """Scrape LinkedIn job listings using Selenium with infinity scroll."""
    driver = init_driver()
    driver.get(url)
    jobs = []
    batch_counter = 0

    try:
        while len(jobs) < num_jobs:
            # Wait for job cards to load
            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-search-card"))
            )
            num_job_cards = len(job_cards)

            for job_card in job_cards[len(jobs) - batch_counter * batch_size:]:
                if len(jobs) >= num_jobs:
                    break

                # Click on the job card to view details
                ActionChains(driver).move_to_element(job_card).click().perform()
                time.sleep(3)

                try:
                    # Extract job details
                    title = driver.find_element(By.CSS_SELECTOR, ".topcard__title").text
                    company = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link").text
                    location = driver.find_element(By.CSS_SELECTOR, ".topcard__flavor--bullet").text

                    # applicants_elements = driver.find_elements(By.CSS_SELECTOR, "figcaption.num-applicants__caption")
                    # applicants = applicants_elements[0].text if applicants_elements else "N/A"

                    applicants_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'applicants')]")
                    applicants = applicants_elements[0].text if applicants_elements else "N/A"

                    time_posted = driver.find_element(By.XPATH, "//span[contains(@class, 'posted-time-ago__text')]").text
                    description = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup").text

                    seniority_level = extract_field(driver, "Seniority level")
                    employment_type = extract_field(driver, "Employment type")
                    job_function = extract_field(driver, "Job function")
                    industries = extract_field(driver, "Industries")

                    job_data = {
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
                    }

                    jobs.append(job_data)
                    print(job_data)

                except Exception as e:
                    print(f"Error processing job card: {e}")
                    continue

                # Save progress every batch_size jobs
                if len(jobs) % batch_size == 0:
                    batch_counter += 1
                    batch_filename = f"jobs_batch_{batch_counter}.json"
                    save_to_json(jobs[-batch_size:], batch_filename)
                    print(f"Saved batch {batch_counter} to {batch_filename}")

            # Scroll or click the "See more jobs" button
            print("Scrolling to load more jobs or clicking the 'See more jobs' button...")
            try:
                # Check for the "See more jobs" button
                see_more_button = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'See more jobs')]"))
                )
                see_more_button.click()  # Click the button to load more jobs
                time.sleep(3)  # Pause to allow the new jobs to load
            except Exception as e:
                print("No 'See more jobs' button found. Scrolling instead.")

                # Fallback to scrolling if no button is found
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                for i in range(3):  # Scroll down in three steps
                    driver.execute_script("window.scrollTo(0, arguments[0]);", (i + 1) * (scroll_height // 3))
                    time.sleep(4)  # Pause for content to load

            # Check if new job cards are loaded
            new_job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
            if len(new_job_cards) == num_job_cards:
                print("Reached the end of the job listings.")
                break  # Exit if no new jobs are loaded

    except KeyboardInterrupt:
        print("Scraping stopped.")
    finally:
        # Save remaining jobs
        if jobs:
            batch_counter += 1
            batch_filename = f"jobs_batch_{batch_counter}.json"
            save_to_json(jobs[-(len(jobs) % batch_size):], batch_filename)
            print(f"Saved remaining jobs to {batch_filename}")
        driver.quit()
        return jobs

def consolidate_json(output_filename):
    """Combine all batch JSON files into a single JSON file."""
    all_files = [f for f in os.listdir() if f.startswith("jobs_batch_") and f.endswith(".json")]
    all_jobs = []

    for file in all_files:
        with open(file, mode="r", encoding="utf-8") as f:
            batch_jobs = json.load(f)
            all_jobs.extend(batch_jobs)

    # Save all jobs to a single JSON file
    if all_jobs:
        save_to_json(all_jobs, output_filename)
        print(f"Consolidated all batches into {output_filename}")

# Usage
if __name__ == "__main__":
    linkedin_jobs_url = "https://www.linkedin.com/jobs/search?keywords=consultant&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    scrape_linkedin_jobs(linkedin_jobs_url, num_jobs=50000, batch_size=100)
    consolidate_json("all_jobs.json")
