import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver


def save_to_csv(jobs, filename):
    """Save a list of jobs to a CSV file."""
    keys = jobs[0].keys() if jobs else []
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)


def scrape_linkedin_jobs(url, num_jobs=1000, batch_size=1000):
    driver = init_driver()
    driver.get(url)
    jobs = []
    batch_counter = 0

    try:
        while len(jobs) + batch_counter*batch_size < num_jobs:  # Stop when the desired number of jobs is reached
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")

            for job_card in job_cards:

                if len(jobs) + batch_counter*batch_size >= num_jobs:  # Check again inside the loop
                    break

                ActionChains(driver).move_to_element(job_card).click().perform()
                time.sleep(1)  # Wait for job details to load

                # Extract job details
                try:
                    title = driver.find_element(By.CSS_SELECTOR, ".topcard__title").text
                    company = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link").text
                    location = driver.find_element(By.CSS_SELECTOR, ".topcard__flavor--bullet").text
                    applicants = driver.find_element(By.CSS_SELECTOR, "figcaption.num-applicants__caption").text
                    time_posted = driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'posted-time-ago__text')]").text

                    description = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup").text

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

                except Exception as e:
                    print(f"Error extracting job details: {e}")

                time.sleep(2)

                # Save progress every batch_size jobs
                if len(jobs) % batch_size == 0:
                    batch_counter += 1
                    batch_filename = f"jobs_batch_{batch_counter}.csv"
                    save_to_csv(jobs[-batch_size:], batch_filename)
                    print(f"Saved batch {batch_counter} to {batch_filename}")

            # Scroll down to load more jobs if needed
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(10)  # Wait for more jobs to load

    except KeyboardInterrupt:
        print("Scraping stopped.")
    finally:
        # Save remaining jobs
        if jobs:
            batch_counter += 1
            batch_filename = f"jobs_batch_{batch_counter}.csv"
            save_to_csv(jobs[-(len(jobs) % batch_size):], batch_filename)
            print(f"Saved remaining jobs to {batch_filename}")
        driver.quit()
        return jobs


def consolidate_csv(output_filename):
    """Combine all batch CSV files into a single CSV."""
    all_files = [f for f in os.listdir() if f.startswith("jobs_batch_") and f.endswith(".csv")]
    all_jobs = []

    for file in all_files:
        with open(file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            all_jobs.extend(list(reader))

    # Save all jobs to a single CSV
    if all_jobs:
        save_to_csv(all_jobs, output_filename)
        print(f"Consolidated all batches into {output_filename}")


# Usage
if __name__ == "__main__":
    linkedin_jobs_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States"
    scrape_linkedin_jobs(linkedin_jobs_url, num_jobs=22, batch_size=5)  # Scrape up to 5,000 jobs in batches
    consolidate_csv("all_jobs.csv")  # Consolidate all batches into one file
