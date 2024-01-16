from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait


LOGIN_URL = "https://campusonline.unir.net/"
HOME_URL = "https://campusonline.unir.net/my/"

USERNAME = "mangelsr25@gmail.com"
PASSWORD = "UNIRM1g4n54N"


FIRST_QUADRIMESTER_SUBJECTS = [
    "Elaboración de Propuestas de Proyectos",
    "Metodología de Diseño y Planificación de Proyectos",
    "Técnicas de Negociación y Resolución de Conflictos",
    "Programas de Financiación Pública y Financiación Privada",
    "Innovación Tecnológica: Definición, Estructura y Gestión",
    "Diseño, Planificación y Negociación de Presupuestos y Recursos",
    "Coaching y Liderazgo en Equipos Distribuidos",
]

SECOND_QUADRIMESTER_SUBJECTS = [
    "Gestión de la calidad, riesgos y evaluación",
    "Implementación, explotación y divulgación de proyectos I+D+i",
    "Metodología de gestión y dirección de proyectos",
    "Legislación de las Tecnologías de la Información y la Comunicación",
    "Auditoría de Proyectos",
]

driver = webdriver.Chrome()


def log_in_site():
    driver.get(LOGIN_URL)

    wait(driver, 20).until(EC.presence_of_element_located((By.ID, "Username")))

    user_element = driver.find_element(By.ID, "Username")
    user_element.send_keys(USERNAME)

    pass_element = driver.find_element(By.NAME, "Password")
    pass_element.send_keys(PASSWORD)

    access_button = driver.find_element(By.ID, "btn-acceder")
    access_button.click()


def get_subject_grade(subject_name: str):
    subject_link = driver.find_element(By.PARTIAL_LINK_TEXT, subject_name)
    subject_link.click()

    grades_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Calificaciones finales")
    grades_link.click()

    need_reprocess = True

    while need_reprocess:
        try:
            wait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//iframe"))
            )
            driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])

            wait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#dinamicTable > tbody > tr:nth-child(3) > td.gb-summary-finalgrade",
                    )
                )
            )
            final_grade = driver.find_element(
                By.CSS_SELECTOR,
                "#dinamicTable > tbody > tr:nth-child(3) > td.gb-summary-finalgrade",
            )

            print(f"{subject_name}: {final_grade.text}")

            driver.switch_to.parent_frame()

            need_reprocess = False
        except:
            driver.refresh()

    driver.get(HOME_URL)


def main():
    log_in_site()
    for subject in SECOND_QUADRIMESTER_SUBJECTS:
        get_subject_grade(subject)
    driver.close()


if __name__ == "__main__":
    main()
