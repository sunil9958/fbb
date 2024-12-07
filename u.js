const axios = require('axios');

const botToken = "7926108528:AAFD-JSvZ2EzZOVE8IK_aiY0F1wy9UV4wpk"; // Replace with your bot token
const accessToken = "Teleservice_36da02c259015c341768052d9a0aa5e69ce2a256dc980e642135b3fe95953544"; // Access token
const admin = "6334683599"; // Replace with your Telegram admin ID

async function sendMessage(message) {
  const url = "https://api.teleservices.io/Broadcast/broadcast/";
  const data = {
    method: "sendMessage",
    text: message,
    access_token: accessToken,
    bot_token: botToken,
    admin: admin,
    type: "text",
    parseMode: "Markdown", // or Markdown
    disableWebPreview: true, // Optional
  };

  try {
    const response = await axios.post(url, data, {
      headers: { "Content-Type": "application/json" },
    });
    console.log("Message sent:", response.data);
  } catch (err) {
    console.error("Error sending message:", err.message);
  }
}
var ms = `🚀 Introducing the Most Advanced TeraBox Downloader Bot! ✉️

🎉 Say hello to @Fastterabox2linkdownbot – your free and unlimited downloader for TeraBox links! 👀

✨ Key Features:
🔹 Free & Unlimited Downloads – Download without any limits!
🔹 24/7 Availability – Access your files anytime, anywhere!
🔹 Fast & Reliable – The fastest TeraBox downloader bot on Telegram!
🔹 Super Easy to Use – Just send the link and get your file in seconds!

🔥 Get ready to experience the most advanced and efficient bot in the entire Telegram community! 🚀

📝 Try it now and enjoy endless downloading at your fingertips!

📲 Start using now: @Fastterabox2linkdownbot`
// Example usage
sendMessage(ms);
