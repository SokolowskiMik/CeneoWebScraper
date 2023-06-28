from app import app
from flask import render_template, request, redirect, url_for, flash
from app.utils import get_element, selectors
import requests
import json
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup


# na 5.0 modele obiektowe zrobic nie trzeba logowania uzytkownikow i kont do 23 czerwca zglosic chec zaliczenia na konsultacjach
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    #dodac obsluge bledow typu niepoprawny kod produktu i litery znaki specjalne
    if request.method == 'POST':
        #wtforms biblioteka do obiektowej walidacji itp
        product_code  = request.form['product_id']
        if 1 != 1:
            flash('Błędne id produktu', category='error')

        else:
            all_opinions = []
            url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
            while(url):
                response =  requests.get(url)
                page = BeautifulSoup(response.text, 'html.parser')
                opinions = page.select("div.js_product-review")
                for opinion in opinions:
                    single_opinion = {}
                    for key, value in selectors.items():
                        single_opinion[key] = get_element(opinion, *value)
                    all_opinions.append(single_opinion)
                try:
                    url = f"https://www.ceneo.pl" + get_element(page, "a.pagination__next", "href")
                except TypeError: 
                    url =  None
            #json
            try:
                os.mkdir("./app/static/opinions")
            except FileExistsError:
                pass
            with open(f"./app/static/opinions/{product_code}.json", 'w', encoding = "UTF-8") as jf:
                json.dump(all_opinions, jf, indent=4, ensure_ascii=False)   
            #csv
            with open(f"./app/static/opinions/{product_code}.csv", 'w', encoding = "UTF-8") as cf:
                dcf = pd.DataFrame(all_opinions)
                dcf.to_csv(f"./app/static/opinions/{product_code}.csv")
            #xlsx
            with open(f"./app/static/opinions/{product_code}.xlsx", 'w', encoding = "UTF-8") as xf:
                df = pd.DataFrame(all_opinions).to_excel(f"./app/static/opinions/{product_code}.xlsx")

            opinions = pd.read_json(json.dumps(all_opinions,ensure_ascii=False))
            opinions.score = opinions.score.map(lambda x: float(x.split("/")[0].replace(",",".")))
            stats = {
                "opinions_count": opinions.shape[0],
                "pros_count": int(opinions.pros.map(bool).sum()),
                "cons_count": int(opinions.pros.map(bool).sum()),
                "avg_score": opinions.score.mean().round(2)

            }

            score = opinions.score.value_counts().reindex(list(np.arange(0, 5.5, 0.5)), fill_value = 0)
            score.plot.bar(color="hotpink")
            plt.xticks(rotation=0)
            plt.title("Histogram ocen")
            plt.xlabel("Liczba gwiazdek")
            plt.ylabel("Liczba opinii")
            plt.ylim(0,max(score.values)+1.5)
            for index, value in enumerate(score):
                plt.text(index, value+0.5, str(value), ha="center")
            try:
                os.mkdir("./app/static/plots")
            except FileExistsError:
                pass
            plt.savefig(f"./app/static/plots/{product_code}_score.png")
            plt.close()

            recommendation = opinions["recommendation"].value_counts(dropna = False).reindex(["Nie polecam", "Polecam", np.nan])
            print(recommendation)
            recommendation.plot.pie(
                label="",
                autopct="%1.1f%%",
                labels= ["Nie polecam", "Polecam", "Nie mam zdania"],
                colors= ["crimson", "forestgreen", "gray"]
            )

            plt.legend(bbox_to_anchor=(1.0,1.0))
            plt.savefig(f"./app/static/plots/{product_code}_recommendation.png")
            plt.close()

            stats['score'] = score.to_dict()
            stats['recommendation'] = recommendation.to_dict()
            try:
                os.mkdir("./app/static/stats")
            except FileExistsError:
                pass
            with open(f"./app/static/stats/{product_code}.json", 'w', encoding = "UTF-8") as jf:
                json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

            return redirect(url_for('product', product_code=product_code))
    return render_template("extract.html")

@app.route('/products', methods=['GET', 'POST'])
def products():
    # lista kodow produktow o ktorych sa pobrane opinie
    # pobranie z pliku json ze statystykami danych do listy slownikow
    # przekazac liste slownikow do szablonu html
    return render_template("products.html")

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<product_code>', methods=['GET', 'POST'])
def product(product_code):

    # pobranie z plikow json opini o produkcie i statystyki do dataframe albo listy slownikow
    # przekazanie opinii i statystyk do szablonu html
    return render_template("product.html", product_code=str(product_code))
