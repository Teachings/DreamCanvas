document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("imageForm");
    const generatedImage = document.getElementById("generatedImage");
    const generateBtn = document.getElementById("generateBtn");
    const spinner = document.getElementById("spinner");
    const buttonText = document.getElementById("buttonText");
    const elapsedTime = document.getElementById("elapsedTime");
    const positivePromptDisplay = document.getElementById("positivePromptDisplay");
    const negativePromptDisplay = document.getElementById("negativePromptDisplay");
    const promptDisplay = document.getElementById("promptDisplay");
    const quickPromptsContainer = document.getElementById("quickPromptsContainer");
    const positiveKeywordsContainer = document.getElementById("positiveKeywords");
    const negativeKeywordsContainer = document.getElementById("negativeKeywords");
    const askLLMButton = document.getElementById("askLLMButton");
    const askLLMSpinner = document.getElementById("askLLMSpinner");
    const askLLMText = document.getElementById("askLLMText");
    const llmResponseTextarea = document.getElementById("llmResponse");
    const useLLMResponseButton = document.getElementById("useLLMResponseButton");
    const notification = document.getElementById("notification");
    const resetBtn = document.getElementById("resetBtn");
    const imageNavigation = document.getElementById("imageNavigation");
    const prevImageBtn = document.getElementById("prevImage");
    const nextImageBtn = document.getElementById("nextImage");

    let timerInterval;
    let startTime;
    let imageHistory = [];  // Cache to store generated images
    let currentImageIndex = -1;  // Current index in image history

    // Function to start the timer
    function startTimer() {
        startTime = new Date().getTime();  // Reset the start time
        elapsedTime.innerText = "(00:00)"; // Reset display time
        elapsedTime.classList.remove("d-none");
        timerInterval = setInterval(function () {
            const now = new Date().getTime();
            const distance = now - startTime;
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            elapsedTime.innerText = `(${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')})`;
        }, 1000);
    }

    // Function to stop the timer
    function stopTimer() {
        clearInterval(timerInterval);
        elapsedTime.classList.add("d-none");
    }

    // Function to display the notification for LLM usage
    function showNotification(message) {
        notification.innerText = message;
        notification.classList.remove("d-none");

        // Hide the notification after 3 seconds
        setTimeout(() => {
            notification.classList.add("d-none");
        }, 3000);
    }

    // Function to reset the form
    resetBtn.addEventListener("click", function () {
        document.getElementById("positivePrompt").value = "";
        document.getElementById("negativePrompt").value = "";
        llmResponseTextarea.value = "";
        generatedImage.classList.add("d-none");
        promptDisplay.classList.add("d-none");
        useLLMResponseButton.classList.add("d-none");
        spinner.classList.add("d-none");
        buttonText.innerText = "Generate Image";
        imageHistory = [];
        currentImageIndex = -1;
        imageNavigation.classList.add("d-none");
        showNotification("The UI has been reset.");
    });

    // Function to dynamically load quick prompts from the server
    function loadQuickPrompts() {
        fetch("/quick_prompts/")
            .then(response => response.json())
            .then(data => {
                quickPromptsContainer.innerHTML = '';  // Clear any existing quick prompts
                positiveKeywordsContainer.innerHTML = '';  // Clear positive prompt buttons
                negativeKeywordsContainer.innerHTML = '';  // Clear negative prompt buttons

                // Load Positive Quick Prompts
                if (data["Positive Quick Prompts"]) {
                    data["Positive Quick Prompts"].forEach(prompt => {
                        const button = document.createElement('button');
                        button.type = 'button';
                        button.classList.add('btn', 'btn-secondary', 'btn-sm', 'me-2', 'mb-2');
                        button.innerText = prompt.label;

                        button.addEventListener('click', function () {
                            addPositiveKeyword(button, prompt.value);
                        });

                        positiveKeywordsContainer.appendChild(button);
                    });
                }

                // Load Negative Quick Prompts
                if (data["Negative Quick Prompts"]) {
                    data["Negative Quick Prompts"].forEach(prompt => {
                        const button = document.createElement('button');
                        button.type = 'button';
                        button.classList.add('btn', 'btn-secondary', 'btn-sm', 'me-2', 'mb-2');
                        button.innerText = prompt.label;

                        button.addEventListener('click', function () {
                            addNegativeKeyword(button, prompt.value);
                        });

                        negativeKeywordsContainer.appendChild(button);
                    });
                }

                // Load Other Quick Prompt Categories (e.g., Halloween, Christmas)
                for (const category in data) {
                    if (category !== "Positive Quick Prompts" && category !== "Negative Quick Prompts") {
                        const section = document.createElement('div');
                        section.classList.add('mb-3');

                        const heading = document.createElement('label');
                        heading.classList.add('form-label');
                        heading.innerText = category;

                        const buttonsContainer = document.createElement('div');
                        buttonsContainer.classList.add('keyword-suggestions');

                        // Generate buttons for each prompt
                        data[category].forEach(prompt => {
                            const button = document.createElement('button');
                            button.type = 'button';
                            button.classList.add('btn', 'btn-secondary', 'btn-sm', 'me-2', 'mb-2');
                            button.innerText = prompt.label;

                            button.addEventListener('click', function () {
                                addPositiveKeyword(button, prompt.value);
                            });

                            buttonsContainer.appendChild(button);
                        });

                        section.appendChild(heading);
                        section.appendChild(buttonsContainer);
                        quickPromptsContainer.appendChild(section);
                    }
                }
            })
            .catch(error => {
                console.error("Error loading quick prompts:", error);
            });
    }

    // Function to add keywords to input fields and disable buttons after selection
    window.addPositiveKeyword = function (button, keyword) {
        const positiveInput = document.getElementById("positivePrompt");
        positiveInput.value = `${positiveInput.value} ${keyword}`.trim();
        button.disabled = true;  // Disable button after adding keyword
    };

    window.addNegativeKeyword = function (button, keyword) {
        const negativeInput = document.getElementById("negativePrompt");
        negativeInput.value = `${negativeInput.value} ${keyword}`.trim();
        button.disabled = true;  // Disable button after adding keyword
    };

    // Function to ask the LLM for a creative prompt
    askLLMButton.addEventListener("click", function () {
        const positivePrompt = document.getElementById("positivePrompt").value;

        let promptToSend = positivePrompt.trim();
        if (!promptToSend) {
            promptToSend = "Generate a general creative idea.";
        }

        // Disable button and show spinner
        askLLMButton.disabled = true;
        askLLMSpinner.classList.remove("d-none");
        askLLMText.innerText = "Processing...";

        fetch("/ask_llm/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ positive_prompt: promptToSend })
        })
        .then(response => response.json())
        .then(data => {
            llmResponseTextarea.value = data.assistant_reply;
            useLLMResponseButton.classList.remove("d-none");  // Show the button to use the LLM's response

            // Re-enable button and hide spinner
            askLLMButton.disabled = false;
            askLLMSpinner.classList.add("d-none");
            askLLMText.innerText = "Ask LLM for Creative Idea";
        })
        .catch(error => {
            console.error("Error getting LLM response:", error);
            askLLMButton.disabled = false;
            askLLMSpinner.classList.add("d-none");
            askLLMText.innerText = "Ask LLM for Creative Idea";
        });
    });

    // Function to use the LLM's creative response as the positive prompt
    useLLMResponseButton.addEventListener("click", function () {
        const llmResponse = llmResponseTextarea.value;
        document.getElementById("positivePrompt").value = llmResponse;
        showNotification("LLM's creative prompt has been applied!");
    });

    // Form submission for generating image
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        // Reset the timer and disable the Generate button
        generateBtn.disabled = true;
        spinner.classList.remove("d-none");
        buttonText.innerText = "Generating...";
        startTimer();  // Start timer with a reset

        // Get input values
        const positivePrompt = document.getElementById("positivePrompt").value;
        const negativePrompt = document.getElementById("negativePrompt").value;
        const steps = document.getElementById("steps").value;
        const width = document.getElementById("width").value;
        const height = document.getElementById("height").value;

        // Post image generation request
        fetch("/generate_images/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                positive_prompt: positivePrompt,
                negative_prompt: negativePrompt,
                steps: parseInt(steps),
                width: parseInt(width),
                height: parseInt(height)
            })
        })
        .then(response => response.blob())
        .then(imageBlob => {
            const imageUrl = URL.createObjectURL(imageBlob);
            generatedImage.src = imageUrl;
            generatedImage.classList.remove("d-none");

            // Cache the image in imageHistory and update the index
            imageHistory.push(imageUrl);
            currentImageIndex = imageHistory.length - 1;
            updateImageNavigation();

            // Display the selected prompts
            positivePromptDisplay.innerText = positivePrompt;
            negativePromptDisplay.innerText = negativePrompt;
            promptDisplay.classList.remove("d-none");

            // Reset the button and timer
            generateBtn.disabled = false;
            spinner.classList.add("d-none");
            buttonText.innerText = "Generate Image";
            stopTimer();
        })
        .catch(error => {
            console.error("Error generating image:", error);
            generateBtn.disabled = false;
            spinner.classList.add("d-none");
            buttonText.innerText = "Generate Image";
            stopTimer();
        });
    });

    // Function to update image navigation visibility and state
    function updateImageNavigation() {
        if (imageHistory.length > 1) {
            imageNavigation.classList.remove("d-none");
        } else {
            imageNavigation.classList.add("d-none");
        }

        prevImageBtn.disabled = currentImageIndex <= 0;
        nextImageBtn.disabled = currentImageIndex >= imageHistory.length - 1;
    }

    // Previous and Next Image Navigation
    prevImageBtn.addEventListener("click", function () {
        if (currentImageIndex > 0) {
            currentImageIndex--;
            generatedImage.src = imageHistory[currentImageIndex];
        }
        updateImageNavigation();
    });

    nextImageBtn.addEventListener("click", function () {
        if (currentImageIndex < imageHistory.length - 1) {
            currentImageIndex++;
            generatedImage.src = imageHistory[currentImageIndex];
        }
        updateImageNavigation();
    });

    // Load quick prompts when the page is loaded
    loadQuickPrompts();
});