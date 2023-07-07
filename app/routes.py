from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.utils import get_element, selectors
from .models import Product, Opinion
from . import db
from .forms import SubmitForm
import requests
import time
import json
import simplejson
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")
from bs4 import BeautifulSoup


#example of product codes 150872408,137671791,39562616,152142703

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = SubmitForm()

    if request.method == 'POST':
        product_code = form.product_id.data
        if form.validate_on_submit():
            all_opinions = []
            url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
            if form.validate_url(url):
                while(url):
                    response =  requests.get(url)
                    page = BeautifulSoup(response.text, 'html.parser')
                    opinions = page.select("div.js_product-review")
                    for opinion in opinions:
                        single_opinion = {}
                        for key, value in selectors.items():
                            single_opinion[key] = get_element(opinion, *value)
                        all_opinions.append(single_opinion)
                        new_opinion = Opinion(opinion_id=single_opinion["opinion_id"], author=single_opinion["author"], recommendation=single_opinion["recommendation"], score=single_opinion["score"], purchased=single_opinion["purchased"], published_at=single_opinion["published_at"], purchased_at=single_opinion["purchased_at"], thumbs_up=single_opinion["thumbs_up"], thumbs_down=single_opinion["thumbs_down"], content=single_opinion["content"], pros=','.join(single_opinion["pros"]), cons=','.join(single_opinion["cons"]), product_code=product_code)
                        db.session.add(new_opinion)
                        db.session.commit()
                    try:
                        url = f"https://www.ceneo.pl" + get_element(page, "a.pagination__next", "href")
                    except TypeError: 
                        url =  None
                if len(all_opinions) == 0:
                    flash('Brak opinii o produkcie', category='error')
                    return redirect(url_for("extract", form=form, product_code=product_code))
            else:
                flash('Błędne id produktu', category='error')
                time.sleep(0.5)
                return redirect(url_for("extract", form=form, product_code=product_code))

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
            with open(f"./app/static/stats/{product_code}.json", 'w', encoding = "UTF-8") as jsf:
                simplejson.dump(stats, jsf, indent=4, ensure_ascii=False, ignore_nan=True)

            new_product = Product(product_code=product_code, opinions_num=stats["opinions_count"], pros=stats["pros_count"], cons=stats["cons_count"], mean_score=stats["avg_score"])
            db.session.add(new_product)
            db.session.commit()

            return redirect(url_for('product', product_code=product_code, ))
        
        else:
            flash('Błędne id produktu', category='error')
            time.sleep(0.5)
            return redirect(url_for("extract", form=form, product_code=product_code))
        
    return render_template("extract.html", form=form)

@app.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.order_by(Product.date_created).all()
    files = os.listdir('app/static/stats')
    product_opinion_list = []
    for f in files:
        with open(f"app/static/stats/{f}", 'r', encoding='utf-8') as jsf:
            js = json.load(jsf)
        product_opinion_list.append((f.split('.')[0],js))
    return render_template("products.html",products=products, p_o_list = product_opinion_list)

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<product_code>', methods=['GET', 'POST'])
def product(product_code):
    product = Product.query.filter_by(product_code=product_code).first()
    with open(f"app/static/opinions/{product_code}.json", 'r', encoding='utf-8') as jsf:
        js = json.load(jsf)
    return render_template("product.html", product_code=product_code, product=product, opinions_list=js)
