import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = 'product_'
WAIT_SECONDS = 10  # Consider defining this as a constant

def get_element(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    return WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.ID, element_id))
    )

@when('I visit the "Home Page"')
def step_impl(context):
    """ Navigate to the base URL """
    context.driver.get(context.base_url)
    logging.info('Visited the home page')

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Verify the page title contains the expected message """
    assert message in context.driver.title, f"Expected title to contain '{message}', but it was '{context.driver.title}'"

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """ Ensure the specified text is not present on the page """
    body_text = context.driver.find_element(By.TAG_NAME, 'body').text
    assert text_string not in body_text, f"Text '{text_string}' should not be present in the body"

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """ Set the value of the input field identified by element_name """
    element = get_element(context, element_name)
    element.clear()
    element.send_keys(text_string)
    logging.info(f'Set the "{element_name}" field to "{text_string}"')

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """ Select an option from a dropdown menu """
    element = Select(get_element(context, element_name))
    element.select_by_visible_text(text)
    logging.info(f'Selected "{text}" in the "{element_name}" dropdown')

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """ Verify the selected option in a dropdown menu """
    element = Select(get_element(context, element_name))
    selected_text = element.first_selected_option.text
    assert selected_text == text, f"Expected '{text}' but found '{selected_text}'"

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """ Verify the input field is empty """
    element = get_element(context, element_name)
    assert element.get_attribute('value') == '', f"The '{element_name}' field is not empty"

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """ Copy the value of an input field to the clipboard """
    element = get_element(context, element_name)
    context.clipboard = element.get_attribute('value')
    logging.info(f'Copied value to clipboard: {context.clipboard}')

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """ Paste the value from the clipboard into an input field """
    element = get_element(context, element_name)
    element.clear()
    element.send_keys(context.clipboard)
    logging.info(f'Pasted value into "{element_name}" field')

@when('I press the "{button}" button')
def step_impl(context, button):
    """ Click the button with the specified name """
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()
    logging.info(f'Pressed the "{button}" button')

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """ Verify that the input field contains the expected text """
    element = get_element(context, element_name)
    assert element.get_attribute('value') == text_string, f"Expected '{text_string}' but found '{element.get_attribute('value')}'"

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """ Change the value of the input field """
    element = get_element(context, element_name)
    element.clear()
    element.send_keys(text_string)
    logging.info(f'Changed "{element_name}" to "{text_string}"')

@then('I should see "{name}" in the results')
def step_impl(context, name):
    """ Verify the search results contain the specified name """
    results_element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.ID, 'search_results'))
    )
    assert name in results_element.text, f"Expected '{name}' to be in the search results"

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """ Ensure the search results do not contain the specified name """
    results_element = context.driver.find_element(By.ID, 'search_results')
    assert name not in results_element.text, f"Expected '{name}' to not be in the search results"

@then('I should see the message "{message}"')
def step_impl(context, message):
    """ Verify that a specific message is displayed """
    flash_message_element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.ID, 'flash_message'))
    )
    assert message in flash_message_element.text, f"Expected flash message '{message}' but found '{flash_message_element.text}'"
