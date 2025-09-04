using System;
using System.Collections.Generic;

namespace AgroSansar.Models
{
    public class WeatherDay
    {
        public string Date { get; set; }
        public string DayName { get; set; }
        public string Condition { get; set; }
        public int AvgTempC { get; set; }
        public int MinTempC { get; set; }
        public int MaxTempC { get; set; }
    }

    public class WeatherForecast
    {
        public string Location { get; set; }
        public WeatherDay Today { get; set; }
        public List<WeatherDay> NextDays { get; set; }
    }
}
