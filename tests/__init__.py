# __init__.py

# # in main folder
# rm dist/SurvSet* 
# python setup.py bdist_wheel --universal

# # on some test conda env
# twine upload --repository-url https://test.pypi.org/legacy/ dist/SurvSet*
# pip uninstall SurvSet
# pip install --index-url https://test.pypi.org/simple/ SurvSet --user

# # Upload to PyPI: https://pypi.org/project/SurvSet/
# twine upload dist/SurvSet*
# pip uninstall SurvSet
# pip install SurvSet
