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

                    activities.append({
                        'type': 'assign',
                        'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text,
                    })

                    continue
                except NoSuchElementException:
                    pass


                # unknown

                activities.append({
                    'type': 'unknown',
                    'text': activity.find_element(By.XPATH, './/span[contains(@class, "instancename")]').text,
                })

            section = {
                'title': titles[i].text,
                'activities': activities,
            }

            response.append(section)

        driver.quit()

        return Response(response)
