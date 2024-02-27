from django.shortcuts import render 
from sentiment_vanilla import ricerca as w

def search_view(request):
    rt1 = w.Search(limit=150, condition="d")
    rt2 = w.Search(limit=150, condition="d" ,advanced=True)
    query_str = request.GET.get('query', '')
    advanced_search = request.GET.get('advanced_search','false')
    if advanced_search == 'true' : # ricerca avanzata
        grouped_results = rt2.search(query_str)
    else:
        grouped_results = rt1.search(query_str)
    return render(request, 'search.html', {"query_str":query_str ,'grouped_results': grouped_results})
