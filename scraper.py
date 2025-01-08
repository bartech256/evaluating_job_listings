import json
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


def save_to_json(jobs, filename):
    """Save a list of jobs to a JSON file."""
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=2, ensure_ascii=False)


def scrape_linkedin_jobs(url, num_jobs=1000, batch_size=1000):
    driver = init_driver()
    driver.get(url)
    jobs = []
    batch_counter = 0

    try:
        while len(jobs) + batch_counter * batch_size < num_jobs:
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")

            for job_card in job_cards:
                if len(jobs) + batch_counter * batch_size >= num_jobs:
                    break

                ActionChains(driver).move_to_element(job_card).click().perform()
                time.sleep(0.5)

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
                    employment_type = driver.find_element(By.XPATH,
                                                          "//li[h3[contains(text(), 'Employment type')]]/span").text
                    job_function = driver.find_element(By.XPATH,
                                                       "//li[h3[contains(text(), 'Job function')]]/span").text
                    industries = driver.find_element(By.XPATH,
                                                     "//li[h3[contains(text(), 'Industries')]]/span").text

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

                except Exception as e:
                    print(f"Error extracting job details: {e}")


                # Save progress every batch_size jobs
                if len(jobs) % batch_size == 0:
                    batch_counter += 1
                    batch_filename = f"jobs_batch_{batch_counter}.json"
                    save_to_json(jobs[-batch_size:], batch_filename)
                    print(f"Saved batch {batch_counter} to {batch_filename}")

            # Scroll down to load more jobs
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)

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
    linkedin_jobs_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States"
    scrape_linkedin_jobs(linkedin_jobs_url, num_jobs=10000, batch_size=100)
    consolidate_json("all_jobs.json")