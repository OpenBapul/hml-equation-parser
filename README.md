# hml-equation-parser

## Usage

If you have `equation string` from `hml` document, you can convert it to latex string by using `eq2latex` function.

```python
>>> import hml_equation_parser as hp
>>> hp.eq2latex("LEFT ⌊ a+b RIGHT ⌋")
'\\left \\lfloor a+b \\right \\rfloor'
```

## Sample code

Let's assume that you have `test.hml` file for converting.
There are some sample code to show how to parse hml documents.
You can refer to this sample codes in `hmlParser.py`(`parseHmlSample`, `convertEquationSample`, `extract2HtmlStrSample`). 

```python
import hml_equation_parser as hp

doc = hp.parseHmlSample("test.hml")  # parse hml document and make ElementTree

doc = hp.convertEquationSample(doc)  # find equations from ElementTree and convert them to latex string
string = hp.extract2HtmlStrSample(doc)  # convert ElementTree to html document with MathJax.

import codecs

f = codecs.open("test.html", "w", "utf8")
f.write(string)
f.close()
```

# hml-equation-parser 한글 문서

## 사용법

`hml`문서에서 수식 `string`을 뽑아냈다면 `eq2latex` 함수를 이용하여 `latex` 수식으로 변환할 수 있습니다.

```python
>>> import hml_equation_parser as hp
>>> hp.eq2latex("LEFT ⌊ a+b RIGHT ⌋")
'\\left \\lfloor a+b \\right \\rfloor'
```

## 예제 코드

hml문서를 파싱하여 전체 문서에서 수식을 바꾸고싶다면 다음 코드를 참조하면 됩니다. 예제에서는 `test.hml`을 파싱하여 html문서로 바꿉니다. 파싱에 대한 더 자세한 내용은 library의 `hmlParser.py` 코드를 참조하세요(`parseHmlSample`, `convertEquationSample`, `extract2HtmlStrSample`).

```python
import hml_equation_parser as hp

doc = hp.parseHmlSample("test.hml")  # parse hml document and make ElementTree

doc = hp.convertEquationSample(doc)  # find equations from ElementTree and convert them to latex string
string = hp.extract2HtmlStrSample(doc)  # convert ElementTree to html document with MathJax.

import codecs

f = codecs.open("test.html", "w", "utf8")
f.write(string)
f.close()
```