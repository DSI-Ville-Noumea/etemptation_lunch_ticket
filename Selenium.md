# Selenium notes

## Find element: 

* by id: 
* by class: 
* by xpath: 
* by text: 
  - by link text: 
  - by partial link text:


### by parent

If nothing is specific for an element, you can find a parent of this element
and start find element from the parent : 

```html
<div id='top'>
    <div id='topa'>
        <a href='#'>link</a>
        <input type='button' />
    </div>
</div>
```

```python
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get('https://example.org')

topa = driver.find_element(By.ID, 'topa')
link = topa.find_element(By.XPATH, '//a').click()
driver.close()
```
