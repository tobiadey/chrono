# Chronofolio (WIP)

Chronofolio is a web application that allows users to upload an image of a watch to predict the brand of the watch, and estimates its price using machine learning models.

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- `pip` package manager
- `virtualenv` for creating virtual environments

### Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
```

2. **Create and activate a virtual environment:**

```bash
make venv
```

3. **Install the required dependencies:**

```bash
make install
```

### Running the Application

1. **Start the Core Server:**

```bash
make server-core
```

2. **Start the BFF (Backend for Frontend) Server:**

```bash
make server-bff

```

3. **Open the Frontend:**

Open frontend/index.html in your web browser to interact with the application.

### Usage

1. Upload an Image:

- Click on the "Choose File" button and select an image of a watch from your local machine.
- Click the "Predict Brand and Price" button.

2. View Results:

- The application will display the predicted brand and price of the watch.
- The uploaded image will also be displayed for reference.

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
