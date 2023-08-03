import os
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
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

        response = []

        for i in range(len(titles)):
            section = {
                'title': titles[i].text,
            }

            response.append(section)

        driver.quit()

        return Response(response)
