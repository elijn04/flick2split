# Flick 2 Split

## Overview
App allows users to upload a photo or a receipt from a restaurant and automatically splits the bill based on what each person ordered, including taxes and tips. 
The app leverages Google Gemini Flash 1.5 for text extraction and provides an intuitive interface for assigning items to individuals.

## Features
- **Upload Receipts:** Users can upload photos or scanned receipts.
- **Text Extraction:** Utilizes Google Gemini Flash 1.5 to extract text from receipts.
- **Item Matching:** Automatically matches items with their respective prices.
- **Interactive Splitting:** Users can assign items to individuals from a dynamic list.
- **Tax and Tip Calculation:** Includes taxes and tips in the final split.

## Technologies Used
- **Frontend & Backend:** Python with Streamlit
- **Text Recognition:** Google Gemini Flash 1.5
- **Development Environment:** Started with Visual Studio Code (VS Code) and switched to Cursor

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/elijn04/flick2split.git
   cd flick2split
   ```

2. **Set Up Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Google Gemini Flash Setup:**
   - Set up access to Google Gemini Flash 1.5 and configure it as per documentation.

## Running the App
1. **Start the App:**
   ```bash
   streamlit run app.py
   ```

2. **Access the App:**
   Open your browser and navigate to the provided localhost address.

## Usage
1. Upload a receipt image via the web interface.
2. The app processes the image, extracts the text, and matches items with their prices.
3. Assign each item to the respective person in the provided list.
4. The app will calculate each individual's total, including tax and tip.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Deployment
- The app is being deployed on **Vercel**. Follow Vercel's documentation to deploy your Streamlit app.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact elijn04@gmail.com.

---

Thank you for using Flick 2 Split! We hope it makes splitting bills with friends and family easier and hassle-free.






