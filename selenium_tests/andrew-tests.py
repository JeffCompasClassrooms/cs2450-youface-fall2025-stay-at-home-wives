import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:8000/map.html")
    #time.sleep(2)

    print("--= Beginning Tests =--")
    mapElement = driver.find_element(By.CSS_SELECTOR, "canvas[id='map']")
    print(mapElement)
    # Get the canvas width
    canvas_width = driver.execute_script("return arguments[0].width;", mapElement)

    # Get the viewport width
    viewport_width = driver.execute_script("return document.querySelector('body').getBoundingClientRect().width;")

    if (canvas_width != viewport_width):
        print(f"[FAIL] - canvas width {canvas_width} != viewport width {viewport_width}")
    else:
        print(f"[SUCCESS] - canvas width {canvas_width} == viewport width {viewport_width}")

    interpolationSuccess = True
    for step in range(1, 10):
        for x in range(-10, 10):
            for y in range(-10, 10):
                hypotenuse = math.sqrt(x ** 2 + y ** 2)
                steps = hypotenuse // step
                interpolation = driver.execute_script("return interpolate([0, 0], arguments[0], arguments[1]);", [x, y], step)
                if (steps == 0):
                    if (interpolation != None):
                        print(f"[FAIL] - interpolate with [{x}, {y}], {step} should have returned `null`")
                        interpolationSuccess = False
                    continue
                failureCount = driver.execute_script("return checkInterpolation(arguments[0], arguments[1]);", interpolation, step)
                if (failureCount != 0):
                    print(f"[FAIL] - checkInterpolation with [{x}, {y}], {step} failed {failureCount} times.")
                    interpolationSuccess = False

    print(f"[SUCCESS] - All interpolations succeeded.")

    pointCount = 10
    points = driver.execute_script("return generateIslandPoints([0,0], arguments[0], 100, 50)", pointCount)

    if (len(points) != pointCount):
        print(f"[FAIL] - len(points) {len(points)} != expected point count {pointCount}")
    else:
        print(f"[SUCCESS] - len(points) {len(points)} == expected point count {pointCount}")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
