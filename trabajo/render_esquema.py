import sys
from playwright.sync_api import sync_playwright
src,out=sys.argv[1],sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':800,'height':1200},device_scale_factor=2.5)
    pg.goto('file://'+src); pg.wait_for_timeout(600)
    el=pg.query_selector('#fig'); el.screenshot(path=out)
    print(el.bounding_box())
    b.close()
