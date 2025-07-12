# Aria Test Suite

## Overview
This directory contains the test suite for Aria. Currently, tests are being developed as part of the Ollama migration.

## Test Structure (Planned)

### Unit Tests
- `test_response_formatter.py` - Test response format conversions
- `test_ollama_client.py` - Test Ollama integration
- `test_utils.py` - Test utility functions
- `test_audio_processing.py` - Test audio handling

### Integration Tests
- `test_conversation_flow.py` - End-to-end conversation tests
- `test_streaming.py` - Streaming response tests
- `test_error_recovery.py` - Error handling tests

### Performance Tests
- `test_latency.py` - Response time measurements
- `test_memory.py` - Memory usage tests

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_response_formatter.py

# Run with coverage
uv run pytest --cov=components tests/
```

## Writing Tests

Tests should follow these guidelines:
1. Use descriptive test names that explain what is being tested
2. Include both positive and negative test cases
3. Mock external dependencies (Ollama API, audio devices)
4. Test edge cases and error conditions

## Test Data

Test fixtures and sample data should be placed in:
- `tests/fixtures/` - Static test data
- `tests/mocks/` - Mock objects and responses

## Current Status

The test suite is being developed as part of the Ollama migration. Initial focus is on:
1. Testing the response format conversion
2. Ensuring streaming functionality is preserved
3. Validating error handling improvements