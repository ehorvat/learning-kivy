import urllib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()

	def search_location(self):
		search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=efb3ad0553cd8021e7193dda6ab572d6"
		search_url = search_template.format(self.search_input.text)
		request = UrlRequest(search_url, self.found_location)

	def found_location(self, request, data):
		cities = [(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings = cities
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()


class CurrentWeather(BoxLayout):
	location = ListProperty(['New York', 'US'])
	conditions = StringProperty()
	temp = NumericProperty()
	temp_min = NumericProperty()
	temp_max = NumericProperty()

	def update_weather(self):
		weather_template = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&APPID=efb3ad0553cd8021e7193dda6ab572d6"
		weather_url = weather_template.format(self.location[0].replace(" ", "%20"), self.location[1])
		request = UrlRequest(weather_url, self.weather_retrieved)

	def weather_retrieved(self, request, data):
		if 'weather' in data:
			self.conditions = data['weather'][0]['description']
			self.temp = data['main']['temp']
			self.temp_min = data['main']['temp_min']
			self.temp_max = data['main']['temp_max']


class LocationButton(ListItemButton):
	location = ListProperty()

class WeatherApp(App):
	pass

class WeatherRoot(BoxLayout):
	location_form = ObjectProperty()
	current_weather = ObjectProperty()

	def __init__(self, **kwargs):
		super(WeatherRoot, self).__init__(**kwargs)
		self.store = JsonStore("weather_store.json")
		if self.store.exists('locations'):
			current_location = self.store.get("locations")["current_location"]
			self.show_current_weather(current_location)

	def show_current_weather(self, location=None):
		self.clear_widgets()

		if self.current_weather is None:
			self.current_weather = CurrentWeather()
		if self.locations is None:
			self.locations = Factory.Locations()
			if (self.store.exists('locations')):
				locations = self.store.get("locations")['locations']
				self.locations.locations_list.adapter.data.extend(locations)

		if location is not None:
			self.current_weather.location = location
			if location not in self.locations.locations_list.adapter.data:
				self.locations.locations_list.adapter.data.append(location)
				self.locations.locations_list._trigger_reset_populate()
				self.store.put("locations", locations=list(self.locations.locations_list.adapter.data), current_location=location)
		self.current_weather.update_weather()
		self.add_widget(self.current_weather)

	def show_location_form(self):
		self.clear_widgets()
		self.add_widget(self.location_form)

	def show_locations(self):
		self.clear_widgets()
		self.add_widget(self.locations)

#This is a module-level function. it exsits in the module, not a class
def locations_args_converter(index, data_item):
	city, country = data_item
	return {'location': (city, country)}

if __name__ == '__main__':
	WeatherApp().run()
