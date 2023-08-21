import math
from django.shortcuts import render
from pysolr import Solr
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from itertools import islice
from django.conf import settings
from spellchecker import SpellChecker

def search(request):
    query = request.GET.get('q', '')
    solr = Solr('http://localhost:8983/solr/mycore/')
    #page_number = request.GET.get('page', 1)
    fields = ["title", "description", "creator", "subject", "date", "language", "identifier", "relation"]

    filters = request.GET.getlist('filter')
    date_filter = request.GET.get('date_filter', '')
    creator_filter = request.GET.get('creator_filter', '')
    language_filter = request.GET.get('language_filter', '')
    spell = SpellChecker()

    if query:
        search_terms = query.split()
        term_queries = []
        for term in search_terms:
            term_queries.extend([f"{field}:{spell.correction(term)}" for field in fields])
            search_query = "(" + " OR ".join(term_queries) + ")"
                                
    else:
        search_query = "*:*"

    if 'date' in filters and date_filter:
        search_query += f" AND date:{date_filter}"
    if 'creator' in filters and creator_filter:
        search_query += f" AND creator:{creator_filter}"
    if 'language' in filters and language_filter:
        search_query += f" AND language:{language_filter}"

    results = solr.search(search_query, rows=100)
    results_list = [result for result in results]

    paginator = Paginator(results_list, 20)  # Number of results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    search_results = []
    for doc in page_obj:
        result = {
            'title': doc.get('title', ''),
            'creator': doc.get('creator', ''),
            'subject': doc.get('subject', ''),
            'description': doc.get('description', ''),
            'date': doc.get('date', ''),
            'identifier': doc.get('identifier', ''),
            'language': doc.get('language', ''),
            'relation': doc.get('relation', ''),
        }
        search_results.append(result)

    context = {
        'results': page_obj,
        'query': query,
        'page_number': page_number,
    }

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if results:
            response_data = {'results': search_results}
        else:
            response_data = {'results': []}
        return JsonResponse(response_data)
    else:
        return render(request, 'search.html', context)



def paginate_search(request):
    query = request.GET.get('q', '')
    solr = Solr('http://localhost:8983/solr/mycore/')
    fields = ["title", "description", "creator", "subject", "date", "language", "identifier", "relation"]

    filters = request.GET.getlist('filter')
    date_filter = request.GET.get('date_filter', '')
    creator_filter = request.GET.get('creator_filter', '')
    language_filter = request.GET.get('language_filter', '')

    if query:
         search_terms = query.split()
         term_queries = []
         for term in search_terms:
            term_queries.extend([f"{field}:{term}" for field in fields])
            search_query = "(" + " OR ".join(term_queries) + ")"
    else:
        search_query = "*:*"
    
    if 'date' in filters and date_filter:
        search_query += f" AND date:{date_filter}"
    if 'creator' in filters and creator_filter:
        search_query += f" AND creator:{creator_filter}"
    if 'language' in filters and language_filter:
        search_query += f" AND language:{language_filter}"

    results = solr.search(search_query, rows=100)
    results_list = [result for result in results]

    paginator = Paginator(results_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    transformed_results = []
    for doc in page_obj:
        result = {
            'title': doc.get('title', ''),
            'creator': doc.get('creator', ''),
            'subject': doc.get('subject', ''),
            'description': doc.get('description', ''),
            'date': doc.get('date', ''),
            'identifier': doc.get('identifier', ''),
            'language': doc.get('language', ''),
            'relation': doc.get('relation', ''),
        }
        transformed_results.append(result)

    response_data = {
        'results': transformed_results,
        'page_number': page_obj.number,
        'paginator': {
            'num_pages':  paginator.num_pages,
        }
    }

    return JsonResponse(response_data)
