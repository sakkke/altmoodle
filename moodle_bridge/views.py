import os
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .utils.moodle import login

# Create your views here.
class Sections(APIView):
    def get(self, request):
        course_id = request.query_params.get('id')

        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)

        login(driver)

        driver.get(os.getenv('MOODLE_URL') + f'/course/view.php?id={course_id}')

        titles = driver.find_elements(By.XPATH, '//h3[@data-for="section_title"]')
        sections = driver.find_elements(By.XPATH, '//li[@data-for="section"]')

        response = []

        for i, section in enumerate(sections):
            activities = []

            for j, activity in enumerate(section.find_elements(By.XPATH, './/li[contains(@class, "activity")]'), 1):
                # assign

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_assign")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'assign',
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text,
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # autoattendmod

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_autoattendmod")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'autoattendmod',

                        # Remove "\n自動出欠" with [:-5]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-5],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # folder

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_folder")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'folder',

                        # Remove "\nフォルダ" with [:-5]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-5],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # forum

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_forum")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'forum',

                        # Remove "\nフォーラム" with [:-6]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-6],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # label

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_label")]')

                    activities.append({
                        'type': 'label',

                        # Remove "完了\n" with [3:]
                        'text': activity.text[3:],
                    })

                    continue
                except NoSuchElementException:
                    pass


                # page

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_page")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'page',

                        # Remove "\nページ" with [:-4]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-4],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # questionnaire

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_questionnaire")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'questionnaire',
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text,
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # resource

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_resource")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'resource',

                        # Remove "\nファイル" with [:-5]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-5],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # url

                try:
                    section.find_element(By.XPATH, f'.//li[position() = {j} and contains(@class, "activity") and contains(@class, "modtype_url")]')

                    description = activity.find_element(By.CLASS_NAME, 'description').text
                    url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                    activities.append({
                        'type': 'url',

                        # Remove "\nURL" with [:-4]
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text[:-4],
                        'description': description,
                        'url': url,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # unknown

                description = activity.find_element(By.CLASS_NAME, 'description').text
                url = activity.find_element(By.XPATH, './/div[@class="activityname"]/a').get_attribute('href')

                activities.append({
                    'type': 'unknown',
                    'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text,
                    'description': description,
                    'url': url,
                })

            section = {
                'title': titles[i].text,
                'activities': activities,
            }

            response.append(section)

        driver.quit()

        return Response(response)
