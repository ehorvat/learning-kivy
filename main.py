from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()

	def search_location(self):
		search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=efb3ad0553cd8021e7193dda6ab572d6" 
		search_url = search_template.format(self.search_input.text)
		request = UrlRequest(search_url, self.found_location)

	def found_location(self, request, data):
		cities = ["{} ({}) Temp: {}".format(d['name'], d['sys']['country'], d['main']['temp']) for d in data['list']]
		self.search_results.item_strings = cities	
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()

class LocationButton(ListItemButton):
	pass

class WeatherApp(App):
	pass

class WeatherRoot(BoxLayout):
	location_form = ObjectProperty()
	def show_current_weather(self, location):
		self.clear_widgets()
		current_weather = Factory.CurrentWeather()
		current_weather.location = location
		self.add_widget(current_weather)
	
	def show_location_form(self):
		self.clear_widgets()
		self.add_widget(self.location_form)

	
if __name__ == '__main__':
	WeatherApp().run()

