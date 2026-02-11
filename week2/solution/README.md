# Week 2 Reference Solution

This directory contains the **completed code** for the Week 2 assignment. It is not a standalone project but rather a set of files you can swap into your main `week2` project to see the working solution.

## How to Run the Solution

1.  **Backup your work**:
    ```bash
    cp week2/app/services/extract.py week2/app/services/extract.py.bak
    cp week2/tests/test_extract.py week2/tests/test_extract.py.bak
    ```

2.  **Copy the Solution Files**:
    ```bash
    cp week2/solution/app/services/extract.py week2/app/services/extract.py
    cp week2/solution/tests/test_extract.py week2/tests/test_extract.py
    ```

3.  **Run the Tests**:
    ```bash
    poetry run pytest week2/tests/test_extract.py
    ```

4.  **Run the App**:
    ```bash
    poetry run uvicorn week2.app.main:app --reload
    ```

## Key Features
-   **Structured Output**: Uses Pydantic `BaseModel` to force JSON output from Ollama.
-   **Mocking**: Tests use `unittest.mock` to simulate LLM responses, ensuring fast and reliable testing.
-   **Error Handling**: The extraction logic safely handles API failures.
