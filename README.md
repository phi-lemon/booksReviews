# BooksReviews

BooksReviews is a Django website to ask for - and create - books reviews. 

## Installation

If you don't have python installed, download and install python from here : https://www.python.org/downloads/

### Get the project files
```bash
git clone https://github.com/phi-lemon/booksReviews.git
```

Create and activate the virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # on windows
source venv/bin/activate  # on linux
```
If you have any problems to activate the virtual environment on windows, 
you may need to authorize scripts execution : `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope process`

Install the dependencies

```bash
pip install -r requirements.txt
```
<br>
The sqlite db is included in the repo with sample data.

## Usage

### Launch Django
```bash
venv\Scripts\activate  # on windows
source venv/bin/activate  # on linux
python manage.py runserver
```

<br>
To see an example of flux, you may log in with the user "george", password "Tititoto44".

## License
[MIT](https://github.com/phi-lemon/booksReviews/blob/main/LICENSE.md)
