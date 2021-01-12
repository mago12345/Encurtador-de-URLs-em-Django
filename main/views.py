from django.shortcuts import render, redirect as django_redirect
from django.http import HttpResponse

from main.models import Link

from random import randint

def random_str():
    alias = ''
    count = 0
    while count < 5:
        alias += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[randint(0, 61)]
        count += 1
    return alias

'''
Faz o redirecionamento de um link encurtado para o link de destino.
'''
def redirect(request, alias):
    try:
        if '+' in alias:
            link = Link.objects.get(alias=alias[0:len(alias)-1])
        else:
            link = Link.objects.get(alias=alias)
        
        # caso o usuário queira as informações do link:
        if alias[-1] == '+':
            return render(request, 'link_info.html', {'dest': link.dest,
                                                      'alias': link.alias,
                                                      'total_views': link.total_views})
        
        link.total_views += 1
        link.save()
        return django_redirect(link.dest)
    except: # caso a página não exista, ou seja, não tenha um link encurtado com o apelido:
        return HttpResponse('Página não encontrada :(')

def index(request):
    return render(request, 'index.html')

def shorten(request):
    dest = request.POST.get('url') # pega o link de destino do novo objeto Link
    
    '''
    Exemplo: usuário digita 'google.com', esse código transforma em 'http://google.com' (em um link completo)
    Obs: em casos como esse, se o site de destino não tiver redirecionamento automático de 'http' para 'https' isso pode ser um problema.
    '''
    if dest[0:7] != 'http://' and dest[0:8] != 'https://':
        dest = 'http://' + dest
    
    # cria o apelido (alias) da url
    while True:
        alias = random_str()
        
        if Link.objects.filter(alias=alias).count() != 0: # se este apelido de url já estiver em uso, tenta outro
            continue
        break
    
    return HttpResponse('http://localhost/' + Link.objects.create(dest=dest, alias=alias).alias) # cria o novo objeto Link e retorna o apelido dele para o usuário
