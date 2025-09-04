using Microsoft.AspNetCore.Mvc;
using AgroSansar.Services;
using AgroSansar.Models;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace AgroSansar.Controllers
{
    public class WeatherController : Controller
    {
        private readonly WeatherService _weatherService;

        public WeatherController(WeatherService weatherService)
        {
            _weatherService = weatherService;
        }

        public async Task<IActionResult> Index(string city = "Kathmandu")
        {
            try
            {
                JObject raw = await _weatherService.GetWeatherAsync(city);
                if (raw == null)
                {
                    ViewBag.Error = "Unable to fetch weather data.";
                    return View(null);
                }

                string locationName = raw["location"]?["name"]?.ToString() ?? city;
                JArray forecastArray = raw["forecast"]?["forecastday"] as JArray;

                if (forecastArray == null || forecastArray.Count == 0)
                {
                    ViewBag.Error = "No forecast data available.";
                    return View(null);
                }

                var forecast = new WeatherForecast
                {
                    Location = locationName,
                    Today = ParseWeatherDay(forecastArray[0]),
                    NextDays = new List<WeatherDay>()
                };

                for (int i = 1; i < forecastArray.Count; i++)
                {
                    forecast.NextDays.Add(ParseWeatherDay(forecastArray[i]));
                }

                return View(forecast);
            }
            catch
            {
                ViewBag.Error = "Unable to fetch weather at the moment. 🫠";
                return View(null);
            }
        }

        private WeatherDay ParseWeatherDay(JToken dayToken)
        {
            DateTime date = DateTime.Parse(dayToken["date"]?.ToString() ?? DateTime.Now.ToString());
            return new WeatherDay
            {
                Date = date.ToString("dd MMM yyyy"),
                DayName = date.DayOfWeek.ToString(),
                Condition = dayToken["day"]?["condition"]?["text"]?.ToString() ?? "N/A",
                AvgTempC = (int?)dayToken["day"]?["avgtemp_c"] ?? 0,
                MinTempC = (int?)dayToken["day"]?["mintemp_c"] ?? 0,
                MaxTempC = (int?)dayToken["day"]?["maxtemp_c"] ?? 0
            };
        }
    }
}
