## JavaScript Methods Documentation for **DreamCanvas**

### Overview
This documentation provides an overview of the key methods in the JavaScript file responsible for handling user interactions, form submissions, image generation, and dynamic prompt loading. It also explains how these methods are connected to the elements defined in the HTML structure.

These JavaScript methods drive the interactive functionality of the **DreamCanvas** app, handling form submissions, prompt input, and dynamic image generation. They are closely connected to the corresponding HTML elements, enabling a smooth and responsive user experience.
---

### **1. `startTimer()`**
**Description:**  
Starts a timer that displays the elapsed time since the image generation process started.

- **How it works:**
  - Captures the current time when the generation process begins.
  - Updates the elapsed time display every second.
  - This is useful to show the user how long the process is taking.

- **Connected HTML Elements:**
  - `elapsedTime`: This element is updated by the method to display the current time in the format `(MM:SS)`.

---

### **2. `stopTimer()`**
**Description:**  
Stops the timer once the image generation process is complete.

- **How it works:**
  - Clears the interval that updates the timer.
  - Hides the timer display by adding the CSS class `d-none`.

- **Connected HTML Elements:**
  - `elapsedTime`: The timer display is hidden after this method is called.

---

### **3. `showNotification(message, type)`**
**Description:**  
Displays a notification to the user with a custom message and type (success or error).

- **Parameters:**
  - `message`: The message to be displayed in the notification.
  - `type`: The type of notification (`success` or `danger`), which determines the visual style of the alert.

- **How it works:**
  - Sets the content and type of the notification element.
  - Automatically hides the notification after 3 seconds.

- **Connected HTML Elements:**
  - `notification`: This is the element where the notification message is displayed.

---

### **4. `resetBtn.addEventListener("click", function () { ... })`**
**Description:**  
Handles the form reset action.

- **How it works:**
  - Clears the input fields for prompts.
  - Hides the image result, prompts, and navigation buttons.
  - Resets the button text and state.
  - Resets any cached image history and disables image navigation.
  - Displays a notification confirming that the form has been reset.

- **Connected HTML Elements:**
  - `positivePrompt` & `negativePrompt`: The input fields for prompts are cleared.
  - `generatedImage`: Hides the generated image.
  - `promptDisplay`: Hides the display of positive and negative prompts.
  - `imageNavigation`: Hides the navigation buttons for switching between images.

---

### **5. `loadQuickPrompts()`**
**Description:**  
Loads quick prompts from the server and populates the respective buttons dynamically.

- **How it works:**
  - Fetches quick prompts (positive, negative, and others) from the server.
  - Dynamically generates buttons based on the prompt categories.
  - Each button, when clicked, adds its respective prompt to the corresponding input field.

- **Connected HTML Elements:**
  - `quickPromptsContainer`: Contains the buttons for different categories of quick prompts.
  - `positiveKeywords` & `negativeKeywords`: Containers for dynamically generated prompt buttons.

---

### **6. `addPositiveKeyword(button, keyword)`**
**Description:**  
Appends a positive keyword to the `positivePrompt` input field when a quick prompt button is clicked.

- **How it works:**
  - Updates the `positivePrompt` input field with the selected keyword.
  - Disables the button after it has been clicked to prevent multiple additions of the same keyword.

- **Connected HTML Elements:**
  - `positivePrompt`: The field where the selected positive prompt keyword is added.

---

### **7. `askLLMButton.addEventListener("click", function () { ... })`**
**Description:**  
Handles the action of asking the LLM (Language Learning Model) for a creative idea based on the current positive prompt.

- **How it works:**
  - Sends the current positive prompt (or a default one) to the server.
  - Displays a spinner to indicate processing.
  - Receives the LLM-generated prompt from the server and updates the `llmResponseTextarea`.
  - Shows the "Use LLM's Creative Prompt" button to allow the user to apply the prompt.

- **Connected HTML Elements:**
  - `positivePrompt`: The input value is sent to the server as part of the request.
  - `llmResponseTextarea`: Displays the response from the LLM.
  - `askLLMSpinner`: Shows the spinner while waiting for the response.
  - `useLLMResponseButton`: Becomes visible once the response is ready.

---

### **8. `useLLMResponseButton.addEventListener("click", function () { ... })`**
**Description:**  
Uses the LLM's generated creative prompt as the positive prompt.

- **How it works:**
  - Copies the content of the `llmResponseTextarea` into the `positivePrompt` input field.
  - Displays a notification confirming that the prompt has been applied.

- **Connected HTML Elements:**
  - `positivePrompt`: Receives the LLM's response as its new value.
  - `llmResponseTextarea`: Source of the creative prompt.

---

### **9. `form.addEventListener("submit", function (event) { ... })`**
**Description:**  
Handles the image generation process when the form is submitted.

- **How it works:**
  - Prevents the default form submission behavior.
  - Disables the "Generate Image" button and starts the spinner and timer.
  - Sends the form data (positive prompt, negative prompt, steps, width, height) to the server.
  - Displays the generated image, updates the image history, and enables navigation buttons for image history.
  - Resets the button and timer after the process is complete.

- **Connected HTML Elements:**
  - `positivePrompt`, `negativePrompt`, `steps`, `width`, `height`: Input fields that send data to the server.
  - `generatedImage`: Displays the generated image.
  - `spinner`: Shows a loading spinner during the process.
  - `buttonText`: Updates the button text to indicate image generation.
  - `imageNavigation`: Shows the image navigation buttons after the image is generated.

---

### **10. `updateImageNavigation()`**
**Description:**  
Updates the state of the previous and next buttons based on the current position in the image history.

- **How it works:**
  - Enables/disables the "Previous" and "Next" buttons depending on whether there are previous/next images in the history.

- **Connected HTML Elements:**
  - `prevImage` & `nextImage`: Navigation buttons to switch between generated images.
  - `imageNavigation`: Shows or hides the entire navigation section.

---

### **11. `prevImageBtn.addEventListener("click", function () { ... })`**
**Description:**  
Navigates to the previous image in the image history when the "Previous" button is clicked.

- **How it works:**
  - Decreases the `currentImageIndex` and updates the `generatedImage` to display the previous image.

- **Connected HTML Elements:**
  - `generatedImage`: Displays the previous image.

---

### **12. `nextImageBtn.addEventListener("click", function () { ... })`**
**Description:**  
Navigates to the next image in the image history when the "Next" button is clicked.

- **How it works:**
  - Increases the `currentImageIndex` and updates the `generatedImage` to display the next image.

- **Connected HTML Elements:**
  - `generatedImage`: Displays the next image.

