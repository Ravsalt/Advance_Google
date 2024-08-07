from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.parse

app = Flask(__name__)
app.secret_key = 'Pogi Si Raven'  # Set a secret key for flash messages

def build_query(params):
    if params.get('type') == 'site':
        return f"site:{params['site']} {params['query']}"
    elif params.get('type') == 'filetype':
        return f"filetype:{params['filetype']} {params['query']}"
    elif params.get('type') == 'exclude':
        return f"{params['query']} -{params['exclude']}"
    elif params.get('type') == 'phrase':
        return f'"{params["phrase"]}"'
    elif params.get('type') == 'title':
        return f'intitle:"{params["title"]}"'
    elif params.get('type') == 'date':
        date_query = f"{params['query']} after:{params['after']}"
        if params.get('before'):
            date_query += f" before:{params['before']}"
        return date_query
    elif params.get('type') == 'or':
        return f"{params['term1']} OR {params['term2']}"
    elif params.get('type') == 'currency':
        return f"{params['query']} {params['price']}"
    elif params.get('type') == 'source':
        return f'{params["query"]} source:{params["source"]}'
    else:
        return params['query']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_type = request.form.get('type')
        
        # Input validation
        if not search_type:
            flash('Please select a search type.', 'error')
            return redirect(url_for('index'))
        
        search_params = {
            'type': search_type,
            'site': request.form.get('site'),
            'filetype': request.form.get('filetype'),
            'query': request.form.get('query'),
            'exclude': request.form.get('exclude'),
            'phrase': request.form.get('phrase'),
            'title': request.form.get('title'),
            'after': request.form.get('after'),
            'before': request.form.get('before'),
            'term1': request.form.get('term1'),
            'term2': request.form.get('term2'),
            'price': request.form.get('price'),
            'source': request.form.get('source'),
        }
        
        # Additional input validation
        if search_type in ['site', 'filetype', 'exclude', 'date', 'currency', 'source'] and not search_params['query']:
            flash('Please enter a search query.', 'error')
            return redirect(url_for('index'))
        
        try:
            search_query = build_query(search_params)
            google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            return render_template('result.html', google_url=google_url)
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

if __name__ == '__main__':
    app.run(debug=False)