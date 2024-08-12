# Chronofolio: Making Time Truly Valuable

Chronofolio is a comprehensive watch portfolio tracker designed to help enthusiasts and collectors manage and monitor the value of their watch collections. As part of our innovative features, users can upload a picture of their watch to receive instant data on its brand and estimated price, powered by advanced machine learning models.

### About Chronofolio:

Chronofolio: Elevating Your Watch Collection

Chronofolio isn't just about tracking value—it's about enhancing your entire experience as a watch collector. With our app, you can easily manage your collection, get detailed insights on individual pieces, and even engage with our AI-powered chatbot, Gemini, to ask questions about your watches or general horological topics. This demo highlights one of Chronofolio's key features: the ability to upload a watch image and get accurate brand identification and price estimates in seconds.

Details of Implemntation at the end of ReadMe. Includes potential questions to ask Chatbot.

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- `pip` package manager
- `virtualenv` for creating virtual environments
- `brew install postgresql`
- `brew services start postgresql`

### Installation

1. **Create and activate a virtual environment:**

```bash
make venv && . env/bin/activate
```

2. **Install the required dependencies:**

```bash
make install
```

3. **Create DB User chronofolio with password chronofolio:**

```bash
createuser -sP chronofolio
```

4. **Create Development DB:**

```bash
createdb -O chronofolio chronofolio_dev
```

5. **Seed Development DB (replace /path/to/export.dump):**

```bash
PGPASSWORD=chronofolio pg_restore -U chronofolio -d chronofolio_dev -j 4 /path/to/export.dump
```

### Running the Application

1. **Start the Core Server:**

```bash
make server
```

2. **Start the Streamlit Server:**

```bash
make streamlit

```

### Usage

1. Upload an Image:

- Click on the "Choose File" button and select an image of a watch from your local machine.
- Click the "Predict Brand and Price" button.

2. View Results:

- The application will display the predicted brand and price of the watch.
- The uploaded image will also be displayed for reference.

3. Chat with app about current watch or other watches

### Development

1. Formatting

```bash
make format

```

2. Linting

```bash
make lint
```

3. Testing

```bash
make test
```

### Potential Questions to ask Chatbot

- Would this be a good investment for the next 10 years?
- How many rolex watches are on here?
- Is the price given for the watch accurate?
- Is selling it for this price a good selling price compared to the market value?
- Give me 5 similar in price watches released in 2022

## Running the Application

### Key Features:

Watch Classification, Price Prediction & Chatbot:

### AI Model:

The core functionality of Chronofolio includes an AI model that classifies the brand of a watch and predicts its price based on an image uploaded by the user. This feature utilises machine learning techniques to provide accurate estimations, making it an invaluable tool for watch collectors and enthusiasts.

### AI Chatbot Powered by Gemini:

LLM Chatbot: Chronofolio integrates an advanced Large Language Model (LLM) chatbot, powered by Gemini, to interact with users. The chatbot allows users to ask detailed questions about their watches or general watch-related inquiries, providing them with tailored, AI-generated responses.
Retrieval Augmented Generation (RAG) with Semantic Routing:

### RAG Architecture:

Chronofolio implements a Retrieval Augmented Generation (RAG) architecture combined with semantic routing to determine how to handle user queries effectively. The system decides whether to use text-to-SQL processing (leveraging Gemini) or to directly answer the user's question based on the context.

### Semantic Routing:

The application employs semantic routing to match user queries with the appropriate response mechanism. It uses predefined routes and a HuggingFaceEncoder to ensure that the system provides accurate and contextually relevant answers, whether it's retrieving data from the database or generating a natural language response.

## How It Works:

Watch Image Upload and Prediction:

Users can upload an image of a watch via the web interface. The application sends the image to a backend service, where the machine learning model predicts the watch's brand and estimates its price. The results are displayed directly on the user interface, offering immediate insights.
Engage with the AI Chatbot:

After receiving the watch's classification and price, users have the option to engage with the AI chatbot. They can ask questions related to the watch, such as its history, market trends, or general watch-related queries. The chatbot, powered by Gemini, provides detailed responses based on the user's input.
RAG and Semantic Routing for Query Handling:

The application uses a RouteLayer with predefined routes to determine how to process each user query. For example, if a user asks for specific data (e.g., "Show me all the watches from Rolex"), the system generates an SQL query to fetch the data from the database. If the query is more general or conversational (e.g., "Tell me about the latest watch trends"), the chatbot generates a direct response.
The application ensures that responses are precise and contextually accurate, enhancing the user's interaction with the system.

### Conclusion:

Chronofolio is a powerful and elegant tool that blends tradition with technology. It offers watch collectors a seamless way to track the value of their collections and provides intelligent, AI-driven insights into their timepieces. Whether it's through precise data retrieval or engaging in rich conversations about watches, Chronofolio makes time truly valuable.

### Chronoflios Capabilites:

Comprehensive Collection Insights
Effortlessly access intricate details, model specifications, and real-time market stats with a single tap, ensuring you’re always informed about your collection.

Market-Driven Alerts
Stay ahead with notifications on trending timepieces, leveraging our extensive market analysis to alert you when certain watches surge in value.

Daily Portfolio Reports
Receive personalised daily summaries detailing the performance and value shifts of your horological assets, helping you make informed decisions.

Detailed Transaction Tracking
Monitor every acquisition and sale with precision, tracking gains and losses to optimize your collection strategy.

Advanced AI Identification
Snap a photo of any watch, and our AI will instantly identify its brand and provide an estimated market value, thanks to our state-of-the-art machine learning models.

AND MORE!
# chrono
