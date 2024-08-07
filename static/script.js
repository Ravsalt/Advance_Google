document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('search-form');
    const typeSelect = document.getElementById('type');
    const additionalFields = document.getElementById('additional-fields');

    typeSelect.addEventListener('change', updateFormFields);
    form.addEventListener('submit', validateForm);

    function updateFormFields() {
        const type = typeSelect.value;
        additionalFields.innerHTML = ''; // Clear previous fields
        
        if (type === 'site') {
            addField('site', 'Website or Domain');
            addField('query', 'Search Query');
        } else if (type === 'filetype') {
            addField('filetype', 'File Type');
            addField('query', 'Search Query');
        } else if (type === 'exclude') {
            addField('query', 'Search Query');
            addField('exclude', 'Term to Exclude');
        } else if (type === 'phrase') {
            addField('phrase', 'Exact Phrase');
        } else if (type === 'title') {
            addField('title', 'Title Phrase');
        } else if (type === 'date') {
            addField('query', 'Search Query');
            addField('after', 'Starting Year');
            addField('before', 'Ending Year (optional)', false);
        } else if (type === 'or') {
            addField('term1', 'First Search Term');
            addField('term2', 'Second Search Term');
        } else if (type === 'currency') {
            addField('query', 'Product');
            addField('price', 'Price');
        } else if (type === 'source') {
            addField('query', 'Search Query');
            addField('source', 'News Source');
        }
    }

    function addField(name, label, required = true) {
        const field = document.createElement('div');
        field.innerHTML = `
            <label for="${name}">${label}:</label>
            <input type="text" name="${name}" id="${name}" ${required ? 'required' : ''}>
        `;
        additionalFields.appendChild(field);
    }

    function validateForm(event) {
        const type = typeSelect.value;
        if (!type) {
            alert('Please select a search type.');
            event.preventDefault();
            return;
        }

        const requiredFields = additionalFields.querySelectorAll('input[required]');
        for (let field of requiredFields) {
            if (!field.value.trim()) {
                alert(`Please fill in the ${field.previousElementSibling.textContent.slice(0, -1)} field.`);
                event.preventDefault();
                return;
            }
        }
    }
});