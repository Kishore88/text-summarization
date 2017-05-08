# Text Summarization
Automatic data summarization is part of machine learning and data mining. The main idea of summarization is to find a subset of data which contains the "information" of the entire set. Such techniques are widely used in industry today

Setting up the Python environment

---
First, install the following packages.

```bash
sudo apt-get install build-essential python-dev python-pip
```

`build-essential` and `python-dev` are used to compile C extensions. Pip is used to install system commands.

Next, install the following Pip packages.

```bash
pip install flask
pip install -r requirements.txt
```

Start the application,
```bash
python run.py
```

You should be able to visit http://localhost:9000/textsummarization.

![Alt text](https://github.com/Kishore88/Text-Summarization/blob/master/static/project-ui.png?raw=true "Optional Title")