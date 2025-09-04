using Microsoft.AspNetCore.Mvc;
using System.Text;
using CsvHelper;
using System.Globalization;

namespace AgroSansar.Controllers;

public class MessageRequest
{
    public string message { get; set; }
}

public class QuestionAnswer
{
    public string question_en { get; set; }
    public string answer_en { get; set; }
    public string question_ne { get; set; }
    public string answer_ne { get; set; }
}

public class ChatbotController : Controller
{
    private const string LangSessionKey = "Language";

    [HttpGet]
    public IActionResult Ask()
    {
        if (string.IsNullOrEmpty(HttpContext.Session.GetString(LangSessionKey)))
            HttpContext.Session.SetString(LangSessionKey, "en");

        ViewBag.CurrentLanguage = HttpContext.Session.GetString(LangSessionKey);
        return View();
    }

    [HttpPost]
    public JsonResult SendMessage([FromBody] MessageRequest data)
    {
        string userMsg = (data.message ?? "").Trim();
        string userMsgLower = userMsg.ToLower();
        string currentLang;

        currentLang = "en";

        if (!string.IsNullOrWhiteSpace(data.message) &&
            data.message.Any(c => c >= '\u0900' && c <= '\u097F'))
        {
            currentLang = "ne";
        }

        if (userMsgLower == "hi" || userMsgLower == "hello")
            return Json(new { reply = currentLang == "ne" ? "नमस्ते! म तपाईंको खेती सहयोगी हुँ।" : "Hello! How can I assist you with your crops today?" });

        if (userMsgLower == "what's your name" || userMsgLower == "whats your name" || userMsgLower == "what is your name")
            return Json(new { reply = currentLang == "ne" ? "म क्रिशीबोट हुँ, तपाईंको AI खेती सहयोगी!" : "I'm KrishiBot, your AI farming assistant!" });

        if (userMsgLower == "how are you")
            return Json(new { reply = currentLang == "ne" ? "म राम्रो छु, तपाईंको बोटबिरुवा बढाउन सहयोग गर्न तयार छु!" : "I'm doing great, ready to help you grow crops!" });

        // Match user message from CSV
        List<string> answers = new List<string>();

        if (currentLang == "ne")
        {
            answers = loadQA.qaList
                .Where(q =>
                    !string.IsNullOrEmpty(q.question_ne) &&
                    (
                        q.question_ne.IndexOf(userMsg, StringComparison.OrdinalIgnoreCase) >= 0 ||
                        userMsg.IndexOf(q.question_ne, StringComparison.OrdinalIgnoreCase) >= 0
                    )
                )
                .Select(q => q.answer_ne)
                .ToList();

        }
        else
        {
            answers = loadQA.qaList
                .Where(q =>
                    !string.IsNullOrEmpty(q.question_en) &&
                    (
                        q.question_en.IndexOf(userMsg, StringComparison.OrdinalIgnoreCase) >= 0 ||
                        userMsg.IndexOf(q.question_en, StringComparison.OrdinalIgnoreCase) >= 0
                    )
                )
                .Select(q => q.answer_en)
                .ToList();

           
        }
        if (answers.Any())
        {
            string reply = string.Join("\n• ", answers);
            return Json(new { reply = "• " + reply });
        }
        return Json(new
        {
            reply = currentLang == "ne"
                ? "🤖 म त यहाँ कृषिसम्बन्धी मात्रै मद्दत गर्न सक्छु। कृपया बाली, बिरुवा, र खेतीसँग सम्बन्धित कुरा सोध्नुहोस्!"
                : "🤖 I wish I could help, but I’m only trained for agriculture questions. Try asking about crops, plants, and farming stuff!"
        });
    }

    [HttpPost]
    public JsonResult ChangeLanguage(string lang)
    {
        if (lang == "en" || lang == "ne")
            HttpContext.Session.SetString(LangSessionKey, lang);

        return Json(new { success = true, lang = lang });
    }

}

public static class loadQA
{
    public static List<QuestionAnswer> qaList;
    public static void LoadCSv()
    {
        qaList = new List<QuestionAnswer>();
        string path = @"C:\DotNet\AgroSansar\AgroSansar\Dataset_chatbot\bilingual_dataset.csv"; // Your CSV path
        using var reader = new StreamReader(path);
        using var csv = new CsvReader(reader, CultureInfo.InvariantCulture);
        qaList = csv.GetRecords<QuestionAnswer>().ToList();

        foreach (var qa in qaList)
        {
            if (!string.IsNullOrEmpty(qa.question_en)) qa.question_en = qa.question_en.ToLower();
            if (!string.IsNullOrEmpty(qa.question_ne)) qa.question_ne = qa.question_ne.ToLower();
        }        
    }
}
