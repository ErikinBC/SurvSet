# __init__.py

# # in main folder
# rm dist/SurvSet* 
# python setup.py bdist_wheel --universal
# twine upload --repository-url https://test.pypi.org/legacy/ dist/SurvSet*

# # on some test conda env
# pip uninstall SurvSet
# pip install --index-url https://test.pypi.org/simple/ pyexample --user

# # Upload to PyPI: https://pypi.org/project/SurvSet/
# twine upload dist/SurvSet*
# pip uninstall SurvSet
# pip install SurvSet
