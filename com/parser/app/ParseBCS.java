package com.parser.app;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

public class ParseBCS {
	Document doc;
	
	
	private void getStrPrice(String link) {
		String sprice = "";
		try {
		Document document = Jsoup.connect(link).get();
		doc = document;
		Elements info = doc.getElementsByClass("quote-head__price-value js-quote-head-price js-price-close");
		} catch (Exception e){
			System.out.println(e);
			}
	}
	
	//получаем иназвание актива
	public String getName(String link) {
		String name = "";
		getStrPrice(link);
		try {
		Elements info = doc.getElementsByClass("quote-head__name");
		name = info.toString();
		name = name.replace("<h1 class=\"quote-head__name\">", "");
		name = name.replace("</h1>", "");
		} catch (Exception e){
			System.out.println(e);
			}
		return name;
	}
	
	//получем измение цены актива с начала дня
	public double getChange() {
		String change = "";
		Double doubleChange = 0.0;
		try {
			Elements info = doc.getElementsByClass("quote-head__price-change js-profit-percent");
			change = info.toString();
			change = change.replace("<div class=\"quote-head__price-change js-profit-percent\">", "");
			change = change.replace(" ", "");
			change = change.replace("</div>", "");
			change = change.replace(",", ".");
			change = change.replace("%", "");
			doubleChange = Double.valueOf(change);
			} catch (Exception e){
				System.out.println(e);
				}
		return doubleChange;
		}
	
	//получаем цену актива
	public double getPrice(){
		double price;
		//String s;
		Elements elemPrice = doc.getElementsByClass("quote-head__price-value js-quote-head-price js-price-close");
		String s = elemPrice.toString();
		s = s.replace("<div class=\"quote-head__price-value js-quote-head-price js-price-close\">", "");
		s = s.replace("</div>", "");
		s = s.replace("&nbsp;", "");
		s = s.replace(",", ".");
		price = Double.parseDouble(s);
		return price;
	}
}
