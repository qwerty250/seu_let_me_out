import time
import tkinter.messagebox

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# CONSTANTS
INFO = ['一卡通', '密码']
FIELDS_1 = ['手机号', '紧急联系人', '紧急联系人手机', '家长', '家长联系电话', '辅导员', '辅导员电话', ]
REASON = '出校原因'
ADDR = '出校地点'
##############

browser = webdriver.Chrome('./webdriver/chromedriver.exe')
browser.implicitly_wait(300)


def find_element_by_data_caption(drv, class_name, caption):
    elements = drv.find_elements_by_class_name(class_name)
    for element in elements:
        if element.get_attribute("data-caption") is None:
            continue
        if element.get_attribute("data-caption").find(caption) >= 0:  # 查找文本
            return element

    return None


def find_element_by_class_keyword(drv, class_name, keyword):
    elements = drv.find_elements_by_class_name(class_name)
    for element in elements:
        if element.text.find(keyword) >= 0:  # 查找文本
            return element

    return None


def find_element_by_css_selector_keyword(drv, css_selector, keyword):
    elements = drv.find_elements_by_css_selector(css_selector)
    for element in elements:
        if element.text.find(keyword) >= 0:  # 查找文本
            return element

    return None


try:
    # 计算离校和返校时间
    # 不指定参数，当天出校
    print('%d arguments received' % len(sys.argv))
    if len(sys.argv) < 2:
        leave_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        back_time = time.strftime("%Y-%m-%d 21:30:00", time.localtime())
        print('leave: %s \t back: %s' % (leave_time, back_time))
    else:   # 指定参数，按照参数进行
        leave_time = sys.argv[1] + " 06:00:00"
        back_time = sys.argv[1] + " 21:30:00"
        print('leave: %s \t back: %s' % (leave_time, back_time))

    browser.maximize_window()
    browser.get('http://ehall.seu.edu.cn/xsfw/sys/xsqjapp/*default/index.do')

    fields = browser.find_elements_by_class_name('auth_input')
    fields[0].send_keys(INFO[0])
    fields[1].send_keys(INFO[1])
    time.sleep(1)

    login_btn = browser.find_elements_by_class_name('auth_login_btn')
    login_btn[0].click()
    time.sleep(0)

    # add
    add_btns = browser.find_elements_by_css_selector("a.bh-btn-primary")
    for i in add_btns:
        if i.get_attribute("data-action") is None:
            continue
        if i.get_attribute("data-action").find("我要请假") >= 0:
            i.click()
            break

    # TODO
    # if browser.find_elements_by_class_name("bh-dialog-title-text") is not None:
    #    tkinter.messagebox.showerror("未能填报", "需要先完成每日打卡。")
    #    browser.quit()

    # time.sleep(5)

    browser.find_element_by_id("CheckCns").click()  # 阅读注意事项并同意
    browser.find_element_by_css_selector("[class='bh-btn bh-btn-primary bh-pull-right']").click()

    # 获取所需的下拉框和字段元素列表
    time.sleep(1)
    dropdowns = browser.find_elements_by_css_selector("[class='jqx-dropdownlist-content jqx-disableselect'] span")
    fields = browser.find_elements_by_css_selector("[class='bh-form-control']")

    # 顺序填写字段

    phone = find_element_by_data_caption(browser, "bh-form-control", "手机号")
    # browser.execute_script("arguments[0].scrollIntoView();", phone)
    phone.click()
    phone.send_keys(Keys.CONTROL, 'a')
    phone.send_keys(Keys.BACKSPACE)
    phone.send_keys(FIELDS_1[0])

    emergency_contact = find_element_by_data_caption(browser, "bh-form-control", "紧急联系人")
    # browser.execute_script("arguments[0].scrollIntoView();", emergency_contact)
    emergency_contact.click()
    emergency_contact.send_keys(Keys.CONTROL, 'a')
    emergency_contact.send_keys(Keys.BACKSPACE)
    emergency_contact.send_keys(FIELDS_1[1])

    emergency_phone = find_element_by_data_caption(browser, "bh-form-control", "紧急联系人电话")
    # browser.execute_script("arguments[0].scrollIntoView();", emergency_phone)
    emergency_phone.click()
    emergency_phone.send_keys(Keys.CONTROL, 'a')
    emergency_phone.send_keys(Keys.BACKSPACE)
    emergency_phone.send_keys(FIELDS_1[2])

    parent = find_element_by_data_caption(browser, "bh-form-control", "家长姓名")
    # browser.execute_script("arguments[0].scrollIntoView();", parent)
    parent.click()
    parent.send_keys(Keys.CONTROL, 'a')
    parent.send_keys(Keys.BACKSPACE)
    parent.send_keys(FIELDS_1[3])

    parent_phone = find_element_by_data_caption(browser, "bh-form-control", "家长联系电话")
    # browser.execute_script("arguments[0].scrollIntoView();", parent_phone)
    parent_phone.click()
    parent_phone.send_keys(Keys.CONTROL, 'a')
    parent_phone.send_keys(Keys.BACKSPACE)
    parent_phone.send_keys(FIELDS_1[4])

    teacher = find_element_by_data_caption(browser, "bh-form-control", "负责老师姓名")
    # browser.execute_script("arguments[0].scrollIntoView();", teacher)
    teacher.click()
    teacher.send_keys(Keys.CONTROL, 'a')
    teacher.send_keys(Keys.BACKSPACE)
    teacher.send_keys(FIELDS_1[5])

    teacher_phone = find_element_by_data_caption(browser, "bh-form-control", "负责老师电话")
    # browser.execute_script("arguments[0].scrollIntoView();", teacher_phone)
    teacher_phone.click()
    teacher_phone.send_keys(Keys.CONTROL, 'a')
    teacher_phone.send_keys(Keys.BACKSPACE)
    teacher_phone.send_keys(FIELDS_1[6])

    dropdowns[0].click()
    time.sleep(1)
    find_element_by_css_selector_keyword(browser, "[class='jqx-listitem-state-normal jqx-item jqx-rc-all']",
                                         "因事出校（当天往返且不离宁）").click()

    dropdowns[1].click()
    time.sleep(1)
    find_element_by_css_selector_keyword(browser, "[class='jqx-listitem-state-normal jqx-item jqx-rc-all']",
                                         "因私").click()

    leave_field = find_element_by_data_caption(browser, "bhtc-input-group", "请假开始日期").find_element_by_tag_name("input")
    browser.execute_script("arguments[0].scrollIntoView();", leave_field)
    find_element_by_css_selector_keyword(browser, "[class ='bh-form-label bh-form-h-label bh-pull-left']",
                                         "请假开始日期").click()
    leave_field.click()
    leave_field.send_keys(leave_time)

    time.sleep(1)

    back_field = find_element_by_data_caption(browser, "bhtc-input-group", "请假结束日期").find_element_by_tag_name("input")
    browser.execute_script("arguments[0].scrollIntoView();", back_field)
    find_element_by_css_selector_keyword(browser, "[class ='bh-form-label bh-form-h-label bh-pull-left']",
                                         "请假结束日期").click()
    back_field.click()
    back_field.send_keys(back_time)

    reason_text = browser.find_element_by_css_selector("[class='bh-txt-input__txtarea']")
    browser.execute_script("arguments[0].scrollIntoView();", reason_text)
    find_element_by_css_selector_keyword(browser, "[class ='bh-form-label bh-form-h-label bh-pull-left']",
                                         "请假详情").click()
    reason_text.click()
    reason_text.send_keys(REASON)

    time.sleep(2)
    browser.execute_script("arguments[0].scrollIntoView();", dropdowns[3])

    dropdowns[3].click()
    time.sleep(1)
    find_element_by_css_selector_keyword(browser, "[class='jqx-listitem-element'] span",
                                         "九龙湖校区").click()

    time.sleep(1)
    find_element_by_css_selector_keyword(browser, "[class ='bh-form-label bh-form-h-label bh-pull-left']",
                                         "是否离开南京").click()

    time.sleep(1)
    dropdowns[4].click()
    time.sleep(1)
    find_element_by_css_selector_keyword(browser, "[class='jqx-listitem-state-normal jqx-item jqx-rc-all']",
                                         "否").click()

    addr_field = find_element_by_data_caption(browser, "jqx-input", "详细地址")
    browser.execute_script("arguments[0].scrollIntoView();", addr_field)
    find_element_by_css_selector_keyword(browser, "[class ='bh-form-label bh-form-h-label bh-pull-left']",
                                         "详细地址").click()
    addr_field.click()
    addr_field.send_keys(ADDR)

    time.sleep(10)

    browser.find_element_by_css_selector("[class='bh-btn bh-btn-primary waves-effect']").click()

    time.sleep(10)
    # tkinter.messagebox.showinfo("成功", "成功出校。")
    browser.quit()

except Exception as e:
    print(e)
    tkinter.messagebox.showerror("未能填报", "出现错误，未能自动出校。请手动操作。")
    browser.quit()
