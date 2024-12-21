/**
 * Generate butter-themed placeholder text directly in Google Sheets.
 * 
 * @param {number} count The number of units to generate (1-10)
 * @param {string} mode The generation mode: "paragraph", "sentence", or "word"
 * @return The generated butter-themed text
 * @customfunction
 */
function BUTTERIPSUM(count = 1, mode = "paragraph") {
  // Validate parameters
  if (count < 1 || count > 10) {
    throw new Error("Count must be between 1 and 10");
  }
  
  const validModes = ["paragraph", "sentence", "word"];
  if (!validModes.includes(mode.toLowerCase())) {
    throw new Error("Mode must be one of: paragraph, sentence, word");
  }
  
  // Call the Butter Ipsum API
  const apiUrl = "https://butteripsum.com/api/v1/generate" +
                "?count=" + encodeURIComponent(count) +
                "&mode=" + encodeURIComponent(mode.toLowerCase());
  
  try {
    const response = UrlFetchApp.fetch(apiUrl, {
      muteHttpExceptions: true,
      timeout: 30
    });
    
    const responseCode = response.getResponseCode();
    if (responseCode !== 200) {
      throw new Error(`HTTP Error ${responseCode}: Failed to fetch text from API`);
    }
    
    const data = JSON.parse(response.getContentText());
    if (data.error) {
      throw new Error(data.message || "API returned an error");
    }
    
    if (!data.text) {
      throw new Error("API response missing text content");
    }
    
    return data.text;
  } catch (error) {
    // Handle specific error types
    if (error.message.includes("Invalid JSON")) {
      throw new Error("Invalid API response format");
    }
    throw new Error("Failed to generate text: " + error.message);
  }
}

/**
 * Example usage in Google Sheets:
 * =BUTTERIPSUM(2, "paragraph")  // Generates 2 paragraphs
 * =BUTTERIPSUM(3, "sentence")   // Generates 3 sentences
 * =BUTTERIPSUM(5, "word")       // Generates 5 words
 */
