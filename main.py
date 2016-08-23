from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()

	def search_location(self):
		search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=efb3ad0553cd8021e7193dda6ab572d6" 
		search_url = search_template.format(self.search_input.text)
		request = UrlRequest(search_url, self.found_location)

	def found_location(self, request, data):
		cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings = cities	

class WeatherApp(App):
    pass

if __name__ == '__main__':
	WeatherApp().run()

