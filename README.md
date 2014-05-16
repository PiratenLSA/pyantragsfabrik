# pyantragsfabrik

Antragsfabrik der Piratenpartei Sachsen-Anhalt

# Dependencies

- git
- python 3
- virtualenv
- pip
- jquery (tested with 1.11.1)

see **requirements.txt**

## Installation

**Prepare:**

```
# git clone https://github.com/PiratenLSA/pyantragsfabrik.git
# cd pyantragsfabrik
# virtualenv env
# . env/bin/activate
# pip install -r requirements.txt
# wget -O antragsfabrik/static/antragsfabrik/javascript/jquery.min.js http://code.jquery.com/jquery-1.11.1.min.js
```

For Python 3 support in **django-markdown-deux** look below.

```
# python manage.py syncdb
# python manage.py migrate
# python manage.py runserver
```

Follow the instructions and open [http://127.0.0.1:8000](http://127.0.0.1:8000). For creating application types or
set social media oauth keys open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Python 3 support in django-markdown-deux

The dependency **django-markdown-deux** has no support for Python 3. To fix this look on GitHub at
[issue #4](https://github.com/trentm/django-markdown-deux/pull/4).

## Updating

```
# git pull origin
# python manage.py syncdb
# python manage.py migrate
```

## License

This Source Code Form is subject to the terms of the **Mozilla Public License, v. 2.0**.

You can find a copy of the MPL in the **LICENSE** file or at [http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/).

Authors:

- Christoph Giesel, Piratenpartei Sachsen-Anhalt