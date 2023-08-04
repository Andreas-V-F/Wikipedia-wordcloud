from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

@ensure_csrf_cookie
def index(request):
    if request.method == "POST":
        words = []
        form = request.POST
        url = form.get("url")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="mw-content-text")
        text = results.find_all("p")
        for t in text:
            words.append(t.get_text().strip().split())
        cleanWords = []
        for word in words:
            for w in word:
                cleanWords.append(w)
                
        string = " ".join(cleanWords)
        wordcloud = WordCloud().generate(string)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        return render(request, "wordcloud.html")
    return render(request, "index.html")


