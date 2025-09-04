using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace AgroSansar.Services
{
    public class WeatherService
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey = "10092fe4cfb74ac284d24142250606"; // replace if needed

        public WeatherService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<JObject> GetWeatherAsync(string city)
        {
            string url = $"http://api.weatherapi.com/v1/forecast.json?key={_apiKey}&q={city}&days=7&aqi=no&alerts=no";
            var response = await _httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            return JObject.Parse(json);
        }
    }
}
