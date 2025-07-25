// Wait for the page (HTML) to fully load before running anything
document.addEventListener("DOMContentLoaded", () => {
  // Grab the form, the input field, and the result area from the page
  const form = document.getElementById("shortenForm");
  const input = document.getElementById("longUrl");
  const result = document.getElementById("result");
  const themeToggle = document.getElementById("themeToggle");

  // פונקציונליות החלפת ערכת נושא
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    themeToggle.textContent = isDark ? "🌞" : "🌙";
  });

  // פונקציה להעתקת טקסט ללוח
  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      // Fallback למדפים ישנים
      const textArea = document.createElement("textarea");
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      return true;
    }
  }

  // פונקציה לבדיקת URL תקין
  function isValidUrl(url) {
    try {
      const urlObj = new URL(url);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  }

  // When the user submits the form
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Stop the page from reloading

    const longUrl = input.value.trim(); // Get the URL the user typed

    // If the user didn't type anything, show an error
    if (!longUrl) {
      result.innerHTML = '<span style="color: #ff5e78;">Please enter a URL.</span>';
      result.classList.remove('has-content');
      return;
    }

    // בדיקת URL תקין
    if (!isValidUrl(longUrl)) {
      result.innerHTML = '<span style="color: #ff5e78;">Please enter a valid URL starting with http:// or https://</span>';
      result.classList.remove('has-content');
      return;
    }

    // הצגת אינדיקטור טעינה
    result.innerHTML = '<span style="color: #007bff;">Shortening your URL...</span>';
    result.classList.remove('has-content');

    try {
      console.log("Sending POST request to Lambda...");
      console.log("URL:", "https://ruzwaoxcbiufiuukrlfrczlt4i0dwpsv.lambda-url.us-west-2.on.aws/");
      console.log("Body:", { url: longUrl });
      
      // Send the URL to the Lambda function using a POST request
      const response = await fetch("https://ruzwaoxcbiufiuukrlfrczlt4i0dwpsv.lambda-url.us-west-2.on.aws/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell the server we're sending JSON
        },
        body: JSON.stringify({ url: longUrl }), // Convert the data to JSON
      });

      console.log("Response received:", response);
      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      // Convert the server's reply into a JavaScript object
      const data = await response.json();
      console.log("Response data:", data);
      console.log("Response data type:", typeof data);
      console.log("Response data keys:", Object.keys(data));

      // If the request worked, show the short URL
      if (response.ok) {
        const shortUrl = `https://ruzwaoxcbiufiuukrlfrczlt4i0dwpsv.lambda-url.us-west-2.on.aws/${data.short_id}`;
        
        // יצירת כפתור העתקה
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '📋 Copy';
        copyButton.onclick = async () => {
          const success = await copyToClipboard(shortUrl);
          if (success) {
            copyButton.innerHTML = '✅ Copied!';
            copyButton.style.background = '#90ee90';
            setTimeout(() => {
              copyButton.innerHTML = '📋 Copy';
              copyButton.style.background = '#007bff';
            }, 2000);
          }
        };

        // יצירת container עם הקישור וכפתור ההעתקה
        const urlContainer = document.createElement('div');
        urlContainer.className = 'url-container';
        
        const urlLink = document.createElement('a');
        urlLink.href = shortUrl;
        urlLink.target = '_blank';
        urlLink.style.color = '#007bff';
        urlLink.style.textDecoration = 'underline';
        urlLink.textContent = shortUrl;
        
        urlContainer.appendChild(urlLink);
        urlContainer.appendChild(copyButton);
        
        result.innerHTML = '<span style="color: #007bff;">Shortened URL:</span>';
        result.appendChild(urlContainer);
        
        // הוספת הרקע האפור
        result.classList.add('has-content');
      } else {
        // If there was an error, show it
        result.innerHTML = `<span style="color: #ff5e78;">Error: ${data.error || "Unexpected error"}</span>`;
        result.classList.remove('has-content');
      }
    } catch (err) {
      // If something goes wrong (e.g., no internet), show a message
      result.innerHTML = `<span style="color: #ff5e78;">Error: ${err.message}</span>`;
    }
  });
});
